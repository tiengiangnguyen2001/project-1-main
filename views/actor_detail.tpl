% rebase('base', title=person["name"], active='actors')

<div class="d-flex justify-content-between align-items-center mb-3">
  <h1 class="h3 mb-0">{{person["name"]}}</h1>
  <a class="btn btn-outline-secondary" href="/actors">Zurück</a>
</div>

<h2 class="h5 mt-4">Filme</h2>

% if len(films) == 0:
  <p class="text-muted">Keine Filme gefunden.</p>
% end

<div class="list-group">
  % for f in films:
    <a class="list-group-item list-group-item-action d-flex justify-content-between align-items-center"
       href="/movie/{{f['id']}}">
      <span>{{f["title"]}}</span>
      <span class="badge bg-secondary rounded-pill">{{f["year"]}}</span>
    </a>
  % end
</div>
