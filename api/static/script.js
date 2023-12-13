const client = filestack.init("AimtGsxwZTyeGl95kwyrrz");
const options = {
    maxFiles: 10,
    onUploadDone: function(data) {
        for (file of data.filesUploaded) {
            let input = document.createElement("input");
            input.setAttribute("type", "hidden");
            input.setAttribute("name", "file-upload");
            input.setAttribute("value", JSON.stringify(file));
            document.getElementById("filestack-handles").appendChild(input);

            let li = document.createElement("li");
            li.innerText = file.filename;
            document.getElementById("uploaded-filenames").appendChild(li);
        }
    }
}

document.getElementById("upload-btn").addEventListener("click", function(event) {
    event.preventDefault();
    client.picker(options).open();
})