% rebase('base', title='Genre', active='genres')

<h1 class="h3 mb-3">Genre</h1>

% if len(genres) == 0:
  <p class="text-muted mt-3">Keine Genres vorhanden.</p>
% end

<div class="list-group">
  % for g in genres:
    <a class="list-group-item list-group-item-action" href="/genre/{{g['id']}}">
      {{g['name']}}
    </a>
  % end
</div>
