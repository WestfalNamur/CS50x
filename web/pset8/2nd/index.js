const newQuestion = () => {
    const li = document.createElement("li");
    const inputValue = document.getElementById("userInput").value;
    const text = document.createTextNode(inputValue);
    li.appendChild(text);
    if (inputValue === '') {
        alert("You must write something.");
    } else {
        document.getElementById("questions").appendChild(li);
    }
}