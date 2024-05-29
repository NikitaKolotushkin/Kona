var currentTab = 0;
showTab(currentTab);

function showTab(tab_index) {
    var tab = document.getElementsByClassName("tab");

    tab[tab_index].style.display = "block";

    if (tab_index == 0) {
        document.getElementById("regPrevBtn").style.display = "none";
    } else {
        document.getElementById("regPrevBtn").style.display = "block";
    }

    if (tab_index == 0) {
        document.getElementById("regNextBtn").innerHTML = "Начнем регистрацию";
    }
}

function changeTab(tab_index) {
    var tab = document.getElementsByClassName("tab");

    if (tab_index == 1 && !validateForm()) {
        return false;
    }

    tab[currentTab].style.display = "none";
    currentTab += tab_index;

    if (currentTab >= tab.length) {
        document.getElementById("regForm").submit();
        return false;
    }

    showTab(currentTab);
}

function validateForm() {
    return 1;
}