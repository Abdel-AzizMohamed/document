let content_container = document.getElementById("article"),
  article_elements = [],
  url = "/api/v1.0/article/",
  id_split = window.location.href.split("/"),
  article_id = id_split[id_split.length - 1];

function parse_list(elements, current_index) {
  let unlist = document.createElement("ul"),
    i = 0;

  for (; i + current_index < elements.length; i++) {
    let element = elements[i + current_index].replaceAll("\r", ""),
      element_text = element.slice(1, element.length);
    if (element[0] != "-") break;

    listElement = document.createElement("li");
    listElement.textContent = element_text;

    unlist.appendChild(listElement);
  }

  return [unlist, i - 1];
}

function parse_heading(element) {
  let heading = element.slice(0, 7);

  for (let i = 0; i < heading.length; i++) {
    if (heading[i] != "#" || i == 6) {
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

function parse_paragraph(elements, current_index) {
  let paragraph = document.createElement("p"),
    i = 0;

  for (; i + current_index < elements.length; i++) {
    let element = elements[i + current_index].replaceAll("\r", "");

    if (["#", "-", "!", "@", "("].includes(element[0]) || !element[0]) break;

    let brElement = document.createElement("br"),
      textNode = document.createTextNode(element);

    paragraph.appendChild(textNode);
    paragraph.appendChild(brElement);
  }

  return [paragraph, i - 1];
}

function parse_code(elements, current_index) {
  let code = document.createElement("pre"),
    i = 1;

  for (; i + current_index < elements.length; i++) {
    let element = elements[i + current_index].replaceAll("\r", "");

    if (element == "```") break;

    let brElement = document.createElement("br"),
      textNode = document.createTextNode(element);

    code.appendChild(textNode);
    code.appendChild(brElement);
  }

  code.classList.add("code-format");

  return [code, i];
}

fetch(`${url}${article_id}`)
  .then((response) => {
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return response.text();
  })
  .then((data) => {
    let article_split = data.split("\n");

    for (let i = 0; i < article_split.length; i++) {
      if (article_split[i] == "\r") continue;
      let element = article_split[i].replaceAll("\r", "");

      if (element[0] == "#") article_elements.push(parse_heading(element));
      else if (element[0] == "@")
        article_elements.push(parse_note(element, "info"));
      else if (element[0] == "!")
        article_elements.push(parse_note(element, "danger"));
      else if (element.slice(0, 3) == "```") {
        let parsed_code = parse_code(article_split, i);
        article_elements.push(parsed_code[0]);
        i += parsed_code[1];
      } else if (element.slice(0, 3) == "---")
        article_elements.push(document.createElement("hr"));
      else if (element[0] == "-") {
        let parsed_list = parse_list(article_split, i);
        article_elements.push(parsed_list[0]);
        i += parsed_list[1];
      } else {
        let parsed_paragraph = parse_paragraph(article_split, i);
        article_elements.push(parsed_paragraph[0]);
        i += parsed_paragraph[1];
      }
    }

    for (let i = 0; i < article_elements.length; i++) {
      content_container.appendChild(article_elements[i]);
    }
  })
  .catch((error) => {
    console.error("Error:", error);
  });
