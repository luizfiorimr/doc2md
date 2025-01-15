from flask import Flask, request, jsonify
from markitdown import MarkItDown

app = Flask(__name__)
markitdown = MarkItDown()


@app.route("/convert", methods=["POST"])
def convert():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        # Save the uploaded file temporarily
        temp_path = f"uploads/temp_{file.filename}"
        file.save(temp_path)

        # Process the file
        result = markitdown.convert(temp_path)

        # Return the result
        return {"content": result.text_content}

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
