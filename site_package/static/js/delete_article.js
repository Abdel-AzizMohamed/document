let deleteButtons = document.querySelectorAll("#delete-article"),
  url = "/api/v1.0/article";

function deleteArticle(article_id, buttonParent) {
  if (confirm("Are you sure you want to delete this article?")) {
    fetch(`${url}/${article_id}`, { method: "DELETE" })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
      })
      .then((_) => {})
      .catch((error) => {
        console.error("Error:", error);
      });
    buttonParent.remove();
  }
}

function hello(username) {
  console.log("hello " + username);
}

for (let i = 0; i < deleteButtons.length; i++) {
  let button = deleteButtons[i],
    article_id = button.dataset.id,
    buttonParent = button.parentElement.parentElement.parentElement;

  button.addEventListener("click", () =>
    deleteArticle(article_id, buttonParent)
  );
}
