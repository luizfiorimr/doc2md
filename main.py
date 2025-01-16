from flask import Flask, request, jsonify
from markitdown import MarkItDown
from openai import OpenAI
from dotenv import load_dotenv
import os
import mimetypes

# Load environment variables
load_dotenv()

# Initialize Flask app
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

        # TODO add language on transcription engine https://github.com/microsoft/markitdown/blob/f58a864951da6c720d3e10987371133c67db296a/src/markitdown/_markitdown.py#L972

        # Process the file
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        md = MarkItDown(llm_client=client, llm_model="gpt-4o")

        mimetype, _ = mimetypes.guess_type(file.filename)
        is_image = mimetype and mimetype.startswith("image/")

        if is_image:
            result = md.convert(
                temp_path,
                llm_prompt="Write a detailed transcription for this image, only text and nothing more.",
            )
        else:
            result = md.convert(temp_path)

        # Return the result
        return {"content": result.text_content}

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
