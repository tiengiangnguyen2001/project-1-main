% rebase('base', title=film["title"], active='movies')

<div class="row g-3">
  <div class="col-12 col-md-4">
    <img class="img-fluid rounded" src="/static/{{film['poster_path']}}" alt="Poster">
  </div>

  <div class="col-12 col-md-8">
    <h1 class="h3 mb-2">{{film["title"]}} ({{film["year"]}})</h1>

    % if film["nation_name"]:
      <div class="mb-3">
        <span class="text-muted">Nation:</span>
        <a class="badge bg-secondary text-decoration-none" href="/nation/{{film['nation_id']}}">
          {{film["nation_name"]}}
        </a>
      </div>
    % end

    % if film["description"]:
      <p>{{film["description"]}}</p>
    % end

    <h2 class="h5 mt-4">Genre</h2>
    % if len(genres) == 0:
      <p class="text-muted">Keine Genres vorhanden.</p>
    % end
    <div class="d-flex flex-wrap gap-2">
      % for g in genres:
        <a class="badge bg-danger text-decoration-none" href="/genre/{{g['id']}}">{{g["name"]}}</a>
      % end
    </div>

    <h2 class="h5 mt-4">Besetzung</h2>
    % if len(cast) == 0:
      <p class="text-muted">Keine Besetzung vorhanden.</p>
    % end
    <div class="list-group">
      % for p in cast:
        <a class="list-group-item list-group-item-action" href="/actor/{{p['id']}}">{{p["name"]}}</a>
      % end
    </div>
  </div>
</div>
