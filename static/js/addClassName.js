const addExcerpt = () => {
	ps = document.getElementsByTagName('p');

	for (let i = 0; i < ps.length; i++) {
		if (ps[i].className === "") {
			ps[i].classList.add("excerpt");
		}

	}
}

addExcerpt();