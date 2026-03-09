% rebase('base', title='Home', active='home')

<div class="p-4 rounded bg-dark text-white mb-3">
  <h1 class="display-5 fw-bold mb-2">KINO</h1>
  <p class="lead mb-4">Willkommen! Nutze die Suche oder klicke auf einen Film.</p>

  <form class="d-flex gap-2" action="/movies" method="get">
    <input class="form-control" type="text" name="q" placeholder="Search Now...">
    <button class="btn btn-danger" type="submit">Go</button>
  </form>
</div>

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
