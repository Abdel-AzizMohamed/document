let content_container = document.getElementById("article");

function parse_list(element) {
  let text = element.slice(1, element.length),
    listElement;

  listElement = document.createElement("li");
  listElement.textContent = text;

  return listElement;
}

function parse_heading(element) {
  let heading = element.slice(0, 6);

  for (let i = 0; i < heading.length; i++) {
    if (heading[i] != "#") {
      let head_element = document.createElement(`h${i}`);
      head_element.textContent = element.slice(i, element.length);

      return head_element;
    }
  }
}

function parse_note(element, ele_class) {
  let text = element.slice(1, element.length),
    noteElement = document.createElement("p");

  noteElement.textContent = text;
  noteElement.classList.add(ele_class);

  return noteElement;
}

function parseContent() {
  let url = "/api/v1.0/article/",
    article_id;

  id_split = window.location.href.split("/");
  article_id = id_split[id_split.length - 1];

  fetch(`${url}${article_id}`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.text();
    })
    .then((data) => {
      let article_elements = [],
        article_split = data.split("\n"),
        element,
        paragrah = document.createElement("p"),
        unlist = document.createElement("ul");

      for (let i = 0; i < article_split.length; i++) {
        if (article_split[i] == "\r") continue;

        element = article_split[i].replaceAll("\r", "");

        if (element[0] == "#") {
          if (paragrah.children.length != 0) {
            article_elements.push(paragrah.cloneNode(true));
            paragrah.textContent = "";
          } else if (unlist.children.length != 0) {
            article_elements.push(unlist.cloneNode(true));
            unlist.textContent = "";
          }
          article_elements.push(parse_heading(element));
        } else if (element[0] == "-") {
          if (paragrah.children.length != 0) {
            article_elements.push(paragrah.cloneNode(true));
            paragrah.textContent = "";
          }
          unlist.appendChild(parse_list(element));
        } else if (element[0] == "@" || element[0] == "!") {
          if (paragrah.children.length != 0) {
            article_elements.push(paragrah.cloneNode(true));
            paragrah.textContent = "";
          } else if (unlist.children.length != 0) {
            article_elements.push(unlist.cloneNode(true));
            unlist.textContent = "";
          }

          let ele_class = element[0] == "@" ? "info" : "danger";

          article_elements.push(parse_note(element, ele_class));
        } else {
          if (unlist.children.length != 0) {
            article_elements.push(unlist);
            unlist.textContent = "";
          }
          paragrah.append(element);
          paragrah.appendChild(document.createElement("br"));
        }
      }

      if (paragrah.children.length != 0) {
        article_elements.push(paragrah.cloneNode(true));
        paragrah.textContent = "";
      } else if (unlist.children.length != 0) {
        article_elements.push(unlist.cloneNode(true));
        unlist.textContent = "";
      }

      for (let i = 0; i < article_elements.length; i++) {
        content_container.appendChild(article_elements[i]);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

parseContent();
