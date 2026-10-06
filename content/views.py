from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import F, Prefetch, Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import activate, get_language, gettext as _
from django.views.decorators.http import require_POST

from .models import Comment, News, Post, Tag

MODELS = {"post": Post, "news": News}


# --------------------------------------------------------------------------- #
#  Listings
# --------------------------------------------------------------------------- #
def _render_list(request, model, kind):
    qs = (
        model.objects.filter(is_published=True)
        .prefetch_related("tags")
        .order_by("-published_at", "-created")
    )

    query = request.GET.get("q", "").strip()
    if query:
        qs = qs.filter(title__icontains=query)

    tag_slug = request.GET.get("tag", "").strip()
    active_tag = Tag.objects.filter(slug=tag_slug).first() if tag_slug else None
    if active_tag:
        qs = qs.filter(tags=active_tag)

    page = Paginator(qs, 9).get_page(request.GET.get("page"))

    context = {
        "kind": kind,
        "page_obj": page,
        "entries": page.object_list,
        "query": query,
        "active_tag": active_tag,
        "all_tags": Tag.objects.all(),
        "meta_title": (
            _("Posts — Ulugbek Umaraliyev") if kind == "post" else _("News — Ulugbek Umaraliyev")
        ),
        "meta_description": (
            _("Articles and notes on web development, Django and Telegram bots.")
            if kind == "post"
            else _("Latest news and updates from Ulugbek Umaraliyev.")
        ),
    }
    return render(request, "content/entry_list.html", context)


def post_list(request):
    return _render_list(request, Post, "post")


def news_list(request):
    return _render_list(request, News, "news")


# --------------------------------------------------------------------------- #
#  Detail
# --------------------------------------------------------------------------- #
def _get_entry(model, slug):
    """Look up a published entry by the active language's slug, then fall back
    to a match in any language (a shared link may use a translated slug while a
    given language has none of its own, so we accept any language's slug)."""
    lang = get_language()
    published = model.objects.filter(is_published=True)
    entry = published.filter(**{f"slug_{lang}": slug}).first()
    if entry is None:
        entry = published.filter(
            Q(slug_uz=slug) | Q(slug_ru=slug) | Q(slug_en=slug)
        ).first()
    if entry is None:
        raise Http404("Entry not found")
    return entry


def _entry_detail(request, model, kind, slug):
    entry = _get_entry(model, slug)

    # Count a view (skip the author's own visits).
    if request.user.is_anonymous or entry.author_id != request.user.id:
        model.objects.filter(pk=entry.pk).update(views=F("views") + 1)

    replies_qs = Comment.objects.select_related("author").order_by("created")
    top_comments = (
        entry.comments.filter(parent__isnull=True)
        .select_related("author")
        .prefetch_related(Prefetch("replies", queryset=replies_qs))
        .order_by("created")
    )

    # Alternate URLs per language (translated slugs) for hreflang / SEO.
    current = get_language()
    alternate_urls = {}
    for code in ("uz", "ru", "en"):
        if getattr(entry, f"slug_{code}", None):
            activate(code)
            alternate_urls[code] = entry.get_absolute_url()
    activate(current)

    context = {
        "kind": kind,
        "entry": entry,
        "top_comments": top_comments,
        "comment_count": entry.comments.count(),
        "meta_title": entry.title,
        "meta_description": entry.meta_description or entry.excerpt,
        "og_image_url": request.build_absolute_uri(entry.poster.url) if entry.poster else None,
        "og_type": "article",
        "alternate_urls": alternate_urls,
        "canonical": entry.get_absolute_url(),
    }
    return render(request, "content/entry_detail.html", context)


def post_detail(request, slug):
    return _entry_detail(request, Post, "post", slug)


def news_detail(request, slug):
    return _entry_detail(request, News, "news", slug)


# --------------------------------------------------------------------------- #
#  Comments
# --------------------------------------------------------------------------- #
@login_required
@require_POST
def comment_create(request, kind, pk):
    model = MODELS.get(kind)
    if model is None:
        return redirect("index")
    target = get_object_or_404(model, pk=pk)

    body = (request.POST.get("body") or "").strip()
    parent_id = request.POST.get("parent") or None
    parent = Comment.objects.filter(pk=parent_id).first() if parent_id else None
    # Flatten threads to a single level (FB/IG style): a reply to a reply is
    # attached to the same top-level comment.
    if parent and parent.parent_id:
        parent = parent.parent

    if not body:
        messages.error(request, _("Comment cannot be empty."))
    else:
        Comment.objects.create(
            author=request.user, body=body, parent=parent, **{kind: target},
        )
        messages.success(request, _("Your comment was posted."))

    return HttpResponseRedirect(target.get_absolute_url() + "#comments")


@login_required
@require_POST
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    # The site owner (staff) may delete any comment; users may delete their own.
    if not (request.user.is_staff or comment.author_id == request.user.id):
        messages.error(request, _("You can't delete this comment."))
        return redirect(comment.target.get_absolute_url() + "#comments")

    target_url = comment.target.get_absolute_url()
    comment.delete()
    messages.success(request, _("Comment deleted."))
    return HttpResponseRedirect(target_url + "#comments")
