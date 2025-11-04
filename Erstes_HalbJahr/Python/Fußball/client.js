document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('fbForm');
    const out = document.getElementById('serverAntwort');

    out.value = '';

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        out.value = 'Sende Anfrage an Server...';

        // FormData erstellen (vor dem Zurücksetzen)
        const formData = new FormData(form);

        // Felder sofort leeren, damit direkt ein neuer Spieler eingetragen werden kann
        form.reset();

        try {
            const url = form.action || window.location.href;
            const res = await fetch(url, { method: 'POST', body: formData });

            const contentType = (res.headers.get('content-type') || '').toLowerCase();
            let text;
            if (contentType.includes('application/json')) {
                const json = await res.json();
                text = JSON.stringify(json, null, 2);
            } else {
                text = await res.text();
            }

            out.value = text;

            // Fokus zurück auf erstes Feld
            const first = document.getElementById('name');
            if (first) first.focus();
        } catch (err) {
            out.value = 'Fehler: ' + (err.message || err);
            console.error(err);
        }
    });
});