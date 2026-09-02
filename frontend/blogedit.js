import { basicSetup, EditorView } from "codemirror";
import { html } from "@codemirror/lang-html";

const editorTheme = EditorView.theme({
    "&": {
        border: "1px solid var(--bs-border-color)",
        borderRadius: "var(--bs-border-radius)",
        fontSize: "0.95rem",
    },
    "&.cm-focused": {
        borderColor: "#86b7fe",
        boxShadow: "0 0 0 0.25rem rgba(13, 110, 253, 0.25)",
        outline: "none",
    },
    ".cm-content": {
        fontFamily: "var(--bs-font-monospace)",
        minHeight: "var(--editor-height)",
    },
    ".cm-scroller": {
        overflow: "auto",
    },
});

function createEditor(textarea) {
    const editorContainer = document.createElement("div");
    editorContainer.className = "code-editor";
    editorContainer.style.setProperty(
        "--editor-height",
        textarea.dataset.editorHeight || "15rem",
    );
    textarea.insertAdjacentElement("afterend", editorContainer);

    const label = textarea.labels?.[0]?.textContent.trim() || "Code editor";

    new EditorView({
        doc: textarea.value,
        parent: editorContainer,
        extensions: [
            basicSetup,
            html(),
            EditorView.lineWrapping,
            editorTheme,
            EditorView.contentAttributes.of({ "aria-label": label }),
            EditorView.updateListener.of((update) => {
                if (update.docChanged) {
                    textarea.value = update.state.doc.toString();
                }
            }),
        ],
    });

    // Keep the WTForms control in the form so its name, submitted value, and
    // server-side validation continue to work. It is only hidden after the
    // CodeMirror instance has initialized successfully.
    textarea.hidden = true;
}

document.querySelectorAll("textarea.code-editor-source").forEach(createEditor);
