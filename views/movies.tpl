% rebase('base', title='Movies', active='movies')

<h1 class="h3 mb-3">Movies</h1>

<form class="row g-2 align-items-end mb-3" action="/movies" method="get">
  <div class="col-12 col-lg-4">
    <label class="form-label">Suche</label>
    <input class="form-control" type="text" name="q" value="{{q}}" placeholder="Film suchen...">
  </div>

  <div class="col-12 col-md-4 col-lg-3">
    <label class="form-label">Genre</label>
    <select class="form-select" name="genre_id">
      <option value="">Alle Genres</option>
      % for g in all_genres:
        % selected = "selected" if str(g["id"]) == str(genre_id) else ""
        <option value="{{g['id']}}" {{selected}}>{{g["name"]}}</option>
      % end
    </select>
  </div>

  <div class="col-12 col-md-4 col-lg-3">
    <label class="form-label">Nation</label>
    <select class="form-select" name="nation_id">
      <option value="">Alle Nationen</option>
      % for n in all_nations:
        % selected = "selected" if str(n["id"]) == str(nation_id) else ""
        <option value="{{n['id']}}" {{selected}}>{{n["name"]}}</option>
      % end
    </select>
  </div>

  <div class="col-6 col-md-2 col-lg-1">
    <label class="form-label">Von</label>
    <input class="form-control" type="text" name="year_from" value="{{year_from}}" placeholder="2000">
  </div>

  <div class="col-6 col-md-2 col-lg-1">
    <label class="form-label">Bis</label>
    <input class="form-control" type="text" name="year_to" value="{{year_to}}" placeholder="2009">
  </div>

  <div class="col-12 col-md-4 col-lg-3">
    <label class="form-label">Sortierung</label>
    <select class="form-select" name="sort">
      <option value="title_asc" {{'selected' if sort=='title_asc' else ''}}>Titel A–Z</option>
      <option value="year_desc" {{'selected' if sort=='year_desc' else ''}}>Jahr neu → alt</option>
      <option value="year_asc" {{'selected' if sort=='year_asc' else ''}}>Jahr alt → neu</option>
    </select>
  </div>

  <div class="col-12 d-flex gap-2">
    <button class="btn btn-danger" type="submit">Anwenden</button>
    <a class="btn btn-outline-secondary" href="/movies">Reset</a>
  </div>
</form>

% if len(movies) == 0:
  <p class="text-muted">Keine Treffer.</p>
% end

<div class="row">
  % for m in movies:
    <div class="col-6 col-md-4 col-lg-3 mb-3">
      <div class="card h-100">
        <img class="card-img-top poster-img" src="/static/{{m['poster_path']}}" alt="Poster">
        <div class="card-body">
          <div class="fw-bold">{{m["title"]}}</div>
          <div class="text-muted">{{m["year"]}}</div>
          <a class="stretched-link" href="/movie/{{m['id']}}"></a>
        </div>
      </div>
    </div>
  % end
</div>
