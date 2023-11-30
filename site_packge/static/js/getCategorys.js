let category = document.getElementById("category"),
  subCategory = document.getElementById("sub-category");

category.onchange = function () {
  let url = "/api/v1.0/sections",
    category_value = category.value;

  subCategory.textContent = "";

  sub_element = document.createElement("option");
  sub_element.value = "None";
  sub_element.textContent = "-";

  subCategory.appendChild(sub_element);

  if (category_value == "None") return;

  fetch(`${url}/${category_value}`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      for (let i = 0; i < data.length; i++) {
        sub_id = i + 1;
        sub_text = data[i][sub_id];

        sub_element = document.createElement("option");
        sub_element.value = sub_id;
        sub_element.textContent = sub_text;

        subCategory.appendChild(sub_element);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
};
