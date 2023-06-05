document.addEventListener("DOMContentLoaded", function () {
	const images = document.querySelectorAll(".text__container p img");
	const titles = document.querySelectorAll(".text__container .article__item_title");
	const text_container = document.querySelectorAll(".text__container")
	const p = document.querySelectorAll(".text__container p");
	const a = document.querySelectorAll(".text__container .btn__link");

	images.forEach((element, index) => {
		const href = element.getAttribute("src");
		const link = document.createElement("a");
		const text = document.createTextNode("img");
		link.setAttribute("href", href);
		link.appendChild(text);

		setClass(link, "article__img_link");

		
		if (p.length > 1) {
			convertToLink(p[index], element, link);
		} else {
			convertToLink(p[0], element, link);
		}

	});

	p.forEach((element, index) => {

		const p = document.createElement("p")

		setClass(p, "main__article_text_container");
		setClass(element, "main__article_text");
		
		moveElement(p, element)
		text_container[index].append(p)


		if (a.length > 1) {
			setClass(a[index], "__read_more");
			moveElement(p, a[index]);
		}

		if (titles.length > 1){
			moveElement(element, titles[index]);
		}else{
			console.log(titles)
			moveElement(element, titles[0]);
		}
	});

	function setClass(element, className) {
		element.classList.add(className);
	}

	function moveElement(parent, child) {
		parent.appendChild(child);
	}

	function convertToLink(parent, imgElement, linkElement) {
		const imgHTML = imgElement.outerHTML;
		const regex = /<img alt="(.*?)" src="(.*?)">/;
		parent.innerHTML = parent.innerHTML.replace(regex, linkElement.outerHTML);
	}
});
