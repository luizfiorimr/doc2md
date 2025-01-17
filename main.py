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
        # Check if content type is provided
        if not request.content_type:
            return jsonify({"error": "Content-Type header is required"}), 400

        # Get the binary data and content type
        file_data = request.get_data()
        content_type = request.content_type

        if not file_data:
            return jsonify({"error": "No file data provided"}), 400

        # Determine file extension from content type
        extension = mimetypes.guess_extension(content_type) or ""
        temp_filename = f"temp_file{extension}"
        temp_path = os.path.join("uploads", temp_filename)

        # Save the binary data to a temporary file
        os.makedirs("uploads", exist_ok=True)
        with open(temp_path, "wb") as f:
            f.write(file_data)

        # TODO add language on transcription engine https://github.com/microsoft/markitdown/blob/f58a864951da6c720d3e10987371133c67db296a/src/markitdown/_markitdown.py#L972

        # Process the file
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        md = MarkItDown(llm_client=client, llm_model=os.getenv("LLM_MODEL", "gpt-4o"))

        is_image = content_type.startswith("image/")

        if is_image:
            result = md.convert(
                temp_path,
                llm_prompt="Write a detailed transcription for this image, only text and nothing more.",
            )
        else:
            result = md.convert(temp_path)

        # Return the result
        return jsonify({"content": result.text_content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
