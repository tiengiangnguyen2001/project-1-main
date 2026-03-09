% setdefault('active', '')

<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <title>{{title or "CineBase"}}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="/static/css/style.css" rel="stylesheet">
</head>
<body>

<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <div class="container">
    <a class="navbar-brand" href="/">CineBase</a>

    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#mainNav">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="mainNav">
      <div class="navbar-nav ms-auto">
        <a class="nav-link {{'active' if active=='home' else ''}}" href="/">Home</a>
        <a class="nav-link {{'active' if active=='movies' else ''}}" href="/movies">Movies</a>
        <a class="nav-link {{'active' if active=='actors' else ''}}" href="/actors">Schauspieler</a>
        <a class="nav-link {{'active' if active=='genres' else ''}}" href="/genres">Genre</a>
        <a class="nav-link {{'active' if active=='nations' else ''}}" href="/nations">Nation</a>
        <a class="nav-link {{'active' if active=='about' else ''}}" href="/about">Über uns</a>
      </div>
    </div>
  </div>
</nav>

<div class="container my-4">
  {{!base}}
</div>

<footer class="bg-dark text-light py-3 mt-5">
  <div class="container d-flex gap-3">
    <a class="text-light" href="/impressum">Impressum</a>
    <a class="text-light" href="/faq">FAQ</a>
  </div>
</footer>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
