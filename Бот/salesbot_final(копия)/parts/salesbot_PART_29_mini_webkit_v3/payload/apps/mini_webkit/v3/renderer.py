
from html import escape

class MiniRenderer:
    def _page(self, title: str, body: str)->str:
        with open(__file__.replace('renderer.py','templates/base.html'), 'r', encoding='utf-8') as f:
            tpl = f.read()
        return tpl.replace('{{TITLE}}', escape(title)).replace('{{BODY}}', body)

    def bundle(self, bundle: dict)->str:
        name = escape(str(bundle.get('name','Bundle')))
        pricing = bundle.get('pricing', {})
        items = bundle.get('items', [])

        pills = ''.join(f'<span class="pill">{escape(i.get("type","item"))}</span>' for i in items)
        rows = ''.join(f"<tr><td>{escape(i.get('type',''))}</td><td>{escape(i.get('desc',''))}</td></tr>" for i in items)

        p_currency = escape(str(pricing.get('currency','KGS')))
        total = pricing.get('total_converted') or pricing.get('total_kgs') or bundle.get('base_price',0)
        p_total = escape(str(total))

        body = f"""
        <h1>Пакет: {name}</h1>
        <div class="row">{pills}</div>
        <table>
          <thead><tr><th>Тип</th><th>Описание</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
        <h2>Итого</h2>
        <div>Сумма: <b>{p_total} {p_currency}</b></div>
        """
        return self._page(f"Bundle — {name}", body)

    def dialog(self, history: list)->str:
        bubbles = []
        for m in history or []:
            role = m.get('role','user')
            cls = 'u' if role=='user' else 'c'
            bubbles.append(f'<div class="bubble {cls}">{escape(str(m.get("content","")))}</div>')
        body = '<h1>Диалог</h1><div class="flex">' + ''.join(bubbles) + '</div>'
        return self._page('Диалог', body)

    def exam(self, report: dict)->str:
        score = report.get('total_score', 0)
        module = escape(str(report.get('module','—')))
        status = 'ok' if score>=20 else ('warn' if score>=10 else 'bad')
        body = f"""
        <h1>Экзамен — результат</h1>
        <div>Модуль: <b>{module}</b></div>
        <div>Баллы: <b class="{status}">{score}</b> / 25</div>
        """
        return self._page('Экзамен — результат', body)
