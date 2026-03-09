% rebase('base', title='Nation', active='nations')

<h1 class="h3 mb-3">Nation</h1>

% if len(nations) == 0:
  <p class="text-muted">Keine Nationen vorhanden.</p>
% end

<div class="list-group">
  % for n in nations:
    <a class="list-group-item list-group-item-action" href="/nation/{{n['id']}}">
      {{n["name"]}}
    </a>
  % end
</div>
