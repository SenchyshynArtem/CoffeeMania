$(document).ready(function () {
  $(".amount").each(function (index, amount) {
    if ($(amount).html() == "1") {
      $(amount).parent().find(".minus").css("color", "grey");
    } else {
      $(amount).parent().find(".minus").css("color", "black");
    }
  });

  $(".change_amount").click(function () {
    const csrf = $("input[name=csrfmiddlewaretoken]").val();
    let product_pk = $(this).parent().parent().find(".product_pk").val();
    let url = $(this).parent().parent().find(".change_amount").val();
    let div = $(this).parent().find(".amount");
    let inner_div = +$(this).parent().find(".amount").html();
    let operation = +$(this).data("value");
    let product_price = $(this).parent().parent().find(".buttons_product .product-price span");
    let default_product_price = +$(this).parent().parent().find(".buttons_product .default_price").val();
    let inner_full_price = $(".full_price_div span");
  
    

    if (inner_div + operation <= 0) {
      div.html("1");
      div.parent().find(".minus").css("color", "grey");
    } else if (inner_div + operation >= 99) {
      div.html("99");
      div.parent().find(".plus").css("color", "grey");
    } else {
      div.html(inner_div + operation);
      div.parent().find(".minus").css("color", "black");
      div.parent().find(".plus").css("color", "black");

      let change_inner_div = +$(this).parent().find(".amount").html();
      $.ajax({
        type: "POST",
        url: url,
        data: {
          csrfmiddlewaretoken: csrf,
          product_pk: product_pk,
          operation: operation,
        },
        success: function () {
          inner_div = inner_div + operation;
          product_price.html(change_inner_div * default_product_price);
          let full_price = 0;
          $(".product-price-basket").each(function (index, price) {
            full_price += +$(price).html();
          });
          inner_full_price.html(full_price);
        },
      });
    }
  });

  // Обработчик клика на кнопку покупки
  $(".buy-button").click(function showBuyModalWindow() {
    // Скрыть кнопку покупки
    $(".buy-button").css("display", "none");
    // Показать модальное окно покупки
    $(".buy-modal-window").css("display", "flex");
    // Создать элемент-затемнитель
    const cover = document.createElement("div");
    cover.classList.add("cover");
    $("main").append(cover);
    // Заблокировать прокрутку страницы
    $("body").css("overflow", "hidden");
  });

  // Обработчик клика на кнопку закрытия модального окна покупки
  $(".close-button").click(function hideBuyModalWindow() {
    // Показать кнопку покупки
    $(".buy-button").css("display", "flex");
    // Скрыть модальное окно покупки
    $(".buy-modal-window").css("display", "none");
    // Удалить элемент-затемнитель
    document.querySelector(".cover").remove();
    // Разблокировать прокрутку страницы
    $("body").css("overflow", "hidden");
  });

  // Обработчик клика на кнопку удаления товара
  $(".product-remove-button").click(function () {
    let updater_url = $(".updater-url").val();
    // Получить CSRF-токен
    const csrf = $("input[name=csrfmiddlewaretoken]").val();
    // Получить идентификатор удаляемого товара
    const pk_product = $(this).val();
    // Отправить AJAX-запрос на удаление товара
    $.ajax({
      type: "POST",
      url: $(".delete-product").val(),
      data: { csrfmiddlewaretoken: csrf, pk_product: pk_product },
      success: function () {
        $.get($(".basket-url").val(), function (data) {
          // Выбор контейнера на другой странице, куда будет отображено содержимое
          let container = $(".modal-basket");
          // Вставка полученного HTML-содержимого в контейнер
          container.html(data);
        });
        $.ajax({
          type: "GET",
          url: updater_url,
          success: (response) => {
            $(".products_amount").html(response.count_product);
          },
        });
      },
    });
  });

  $(".close_basket").click(function () {
    $(".modal-basket").css("display", "none");
    $("body").css("overflow", "auto");
    $(".modal-basket-cloth").css("display", "none");
    $("body").css("overflow-x", "hidden");
  });

  $(".modal-basket-cloth").click(function () {
    $(".modal-basket").css("display", "none");
    $("body").css("overflow", "auto");
    $(".modal-basket-cloth").css("display", "none");
    $("body").css("overflow-x", "hidden");
  });
});
