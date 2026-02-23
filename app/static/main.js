document.addEventListener("DOMContentLoaded", () => {
    // Pin toggle — fetch POST, update button without reload
    document.querySelectorAll(".pin-toggle").forEach((btn) => {
        btn.addEventListener("click", async () => {
            const noteId = btn.dataset.noteId;
            const res = await fetch(`/notes/${noteId}/pin`, { method: "POST" });
            if (res.ok) {
                location.reload();
            }
        });
    });

    // Delete confirmation
    document.querySelectorAll(".delete-form").forEach((form) => {
        form.addEventListener("submit", (e) => {
            if (!confirm("Удалить заметку?")) {
                e.preventDefault();
            }
        });
    });
});
