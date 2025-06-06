from base64 import b64encode
from flask import Flask, render_template, redirect, url_for, request
from .handler import SITLHandler, ImageStatus

def create_app(handler: SITLHandler) -> Flask:
    app = Flask(
        import_name=__name__,
        template_folder="templates",
        static_folder="static",
        static_url_path="/static"
    )

    @app.route("/")
    def index():
        return redirect(url_for("next_queue"))

    @app.route("/save", methods=["POST"])
    def save():
        if not handler.save():
            return "Error saving changes", 500

        if "id" not in request.form or not request.form["id"].isdigit():
            return "Save successful", 200

        return redirect(url_for("item", id=request.form["id"]))

    @app.route("/prev", methods=["POST"])
    def prev():
        if "id" not in request.form or not request.form["id"].isdigit():
            return "Bad Request", 400

        if (id := int(request.form["id"])) <= 0:
            return redirect(url_for("item", id=0))

        return redirect(url_for("item", id=id - 1))

    @app.route("/next-queue")
    def next_queue():
        next_id = handler.next_queue()
        if next_id is None:
            return "No more items in queue", 404

        return redirect(url_for("item", id=next_id))

    @app.route("/next", methods=["POST"])
    def next():
        if "id" not in request.form or not request.form["id"].isdigit():
            return "Bad Request", 400

        if (id := int(request.form["id"])) >= len(handler) - 1:
            return redirect(url_for("item", id=len(handler) - 1))

        return redirect(url_for("item", id=id + 1))

    @app.route("/pass", methods=["POST"])
    def pass_item():
        if "id" not in request.form or not request.form["id"].isdigit() or "text" not in request.form:
            return "Bad Request", 400

        id = int(request.form["id"])
        if not handler.set(id, request.form["text"], ImageStatus.PASS):
            return "Error updating item", 500

        return redirect(url_for("next_queue"))

    @app.route("/drop", methods=["POST"])
    def drop_item():
        if "id" not in request.form or not request.form["id"].isdigit() or "text" not in request.form:
            return "Bad Request", 400

        id = int(request.form["id"])
        if not handler.set(id, request.form["text"], ImageStatus.DROP):
            return "Error updating item", 500

        return redirect(url_for("next_queue"))

    @app.route("/fix", methods=["POST"])
    def fix_item():
        if "id" not in request.form or not request.form["id"].isdigit() or "text" not in request.form:
            return "Bad Request", 400

        id = int(request.form["id"])
        if not handler.set(id, request.form["text"], ImageStatus.FIX):
            return "Error updating item", 500

        return redirect(url_for("next_queue"))

    @app.route("/<int:id>")
    def item(id: int):
        item = handler.get(id)
        if item is None:
            return "Not Found", 404

        images = [(name, b64encode(image).decode('utf-8')) for name, image in item.images]
        stats = handler.stats()

        return render_template(
            "item.html",
            name=handler.name,
            id=id,
            images=images,
            status=item.status.name,
            text=item.text,
            stats=stats,
            size=item.size,
            file=item.file
        )

    return app
