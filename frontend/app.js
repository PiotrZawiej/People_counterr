"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
document.addEventListener("DOMContentLoaded", () => {
    const uploadForm = document.getElementById("upload-form");
    const fileInput = document.getElementById("image-upload");
    const responseDiv = document.getElementById("upload-response");
    uploadForm.addEventListener("submit", (event) => __awaiter(void 0, void 0, void 0, function* () {
        event.preventDefault();
        if (!fileInput.files || fileInput.files.length === 0) {
            responseDiv.textContent = "Please select a file before submitting.";
            return;
        }
        const formData = new FormData();
        formData.append("file", fileInput.files[0]);
        try {
            const res = yield fetch("http://localhost:8000/upload_image", {
                method: "POST",
                body: formData,
            });
            if (!res.ok) {
                throw new Error("An error occurred while uploading the file.");
            }
            const data = yield res.json();
            responseDiv.innerHTML = `
                <strong>Image successfully sent for processing!</strong><br>
                <strong>Event ID:</strong> <code>${data.eventid}</code><br>
                <strong>Status:</strong> ${data.status}
            `;
        }
        catch (err) {
            if (err instanceof Error) {
                responseDiv.textContent = "Error: " + err.message;
            }
            else {
                responseDiv.textContent = "An unknown error occurred.";
            }
        }
    }));
});
