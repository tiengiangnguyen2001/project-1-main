% rebase('base', title=nation["name"], active='nations')

<div class="d-flex justify-content-between align-items-center mb-3">
  <h1 class="h3 mb-0">Nation: {{nation["name"]}}</h1>
  <a class="btn btn-outline-secondary" href="/nations">Zurück</a>
</div>

% if len(movies) == 0:
  <p class="text-muted">Keine Filme für diese Nation.</p>
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
