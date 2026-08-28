document.addEventListener("DOMContentLoaded", function () {

    const messages = document.querySelectorAll(".message");

    messages.forEach(function (message) {
        setTimeout(function () {
            message.style.opacity = "0";
            message.style.transform = "translateY(-10px)";

            setTimeout(function () {
                message.remove();
            }, 300);

        }, 3500);
    });


    const productCards = document.querySelectorAll(".product-card");

    productCards.forEach(function (card) {

        card.addEventListener("mouseenter", function () {
            card.style.transition = "transform 0.25s ease";
        });

    });

});