
const naviagte = (element) => {
    const selectedPageId = element.id
    const activePageId = document.querySelector('.activePage').id;
    document.getElementById(activePageId).classList.add('inactivePage');
    document.getElementById(activePageId).classList.remove('activePage');
    document.getElementById(selectedPageId).classList.add('activePage');
    document.getElementById(selectedPageId).classList.remove('inactivePage');


    console.log(element.id, activePageId);
}


