let category = document.getElementById("category"),
  subCategory = document.getElementById("sub-category"),
  url = "/api/v1.0/sections";

category.onchange = function () {
  subCategory.textContent = "";

  sub_element = document.createElement("option");
  sub_element.value = "None";
  sub_element.textContent = "-";
  subCategory.appendChild(sub_element);

  if (category.value == "None") return;

  fetch(`${url}/${category.value}`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      for (let i = 0; i < data.length; i++) {
        sub_id = data[i][0];
        sub_text = data[i][1];

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
