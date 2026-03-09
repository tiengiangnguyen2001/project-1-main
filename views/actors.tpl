% rebase('base', title='Schauspieler', active='actors')

<h1 class="h3 mb-3">Schauspieler</h1>

<form class="d-flex gap-2 mb-3" action="/actors" method="get">
  <input class="form-control" type="text" name="q" value="{{q}}" placeholder="Schauspieler suchen...">
  <button class="btn btn-danger" type="submit">Suchen</button>
  <a class="btn btn-outline-secondary" href="/actors">Reset</a>
</form>

% if len(people) == 0:
  <p class="text-muted">Keine Treffer.</p>
% end

<div class="list-group">
  % for p in people:
    <a class="list-group-item list-group-item-action" href="/actor/{{p['id']}}">
      {{p["name"]}}
    </a>
  % end
</div>
