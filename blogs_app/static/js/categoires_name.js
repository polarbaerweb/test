document.addEventListener("DOMContentLoaded", function(){
	const links__container_title = document.querySelector(".links__container_title")
	const categories__container = document.querySelector(".categories__container")

	links__container_title.addEventListener("click", function(){
		categories__container.classList.toggle("__active")
	})
})