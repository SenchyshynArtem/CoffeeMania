

$(document).ready(function () {

  // Добавление класса "active" к активному пункту меню
  $(".menu-burger-button").each(function () {
    if (window.location.href === $(this).prop("href")) {
      $(this).css('border-bottom', '3px solid #85DB9D');
      $(this).css("justify-content", "end");
      $(this).css("padding", "0 0 0 10px");
    }
  });

  $(".burger_menu").click(function () {
    $('main').css("overflow", "hidden")
    $('body').css("overflow", "hidden") 
    $('.inner_header_burger ').css('left', '0')
  })

  $('.burger_cross span').click(function() {
    $('.inner_header_burger ').css('left', '-100%')
    $('main').css("overflow-y", "scroll")
    $('body').css("overflow-y", "scroll")
  })


  // Добавление класса "active" к активному пункту меню
  $(".menu-button").each(function () {
    if (window.location.href === $(this).prop("href")) {
      $(this).addClass("active");
    }
  });

  $(".plus-main").click(function (){
    let amount = $(this).parent().find(".amount");
    let amount_input = $(this).parent().parent().find(".amount-input");
    if (amount.html() > 99) {
      amount.html(99)
      amount_input.html(99)
    } else if (amount.html() < 99) {
      amount.html(+amount.html() + 1)
      amount_input.val(amount.html())
    };
  });
  $(".minus-main").click(function (){
    let amount = $(this).parent().find(".amount");
    let amount_input = $(this).parent().parent().find(".amount-input");
    if (amount.html() < 1) {
      amount.html(1)
      amount_input.html(1)
    } else if (amount.html() > 1) {
      amount.html(+amount.html() - 1)
      amount_input.val(amount.html())
    };
  });

  $(".change-amount-main").click(function () {
    let default_price = +$(this).parent().find(".default-price").val()
    let inner_full_price = $(".product-totalprice span")
    let amount_product = +$(this).parent().find(".amount").html()
    $(inner_full_price).html(amount_product * default_price)
  });
  

  // Обработчик клика на кнопке добавления товара
  $(".add-product-button").click(function (e) {
    e.preventDefault();
    
    const csrf = $("input[name=csrfmiddlewaretoken]").val();
    let amount = $(this).parent().find(".amount-input").val();
    let product_pk = $(this).parent().find('[class="product-pk"]').val();
    let url = $(this).parent().find('.product-url').val();
    let updater_url = $('.updater-url').val();
    // Сохраняем ссылку на текущий элемент
    let addButton = $(this);

    $.ajax({
      type: "POST",
      url: url,
      data: { csrfmiddlewaretoken: csrf, product_pk: product_pk, amount:amount},
      success: function (response) {
        addButton.attr("src", addButton.siblings(".add_in_basket").val());
        setTimeout(function () {
          addButton.attr("src", addButton.siblings(".default_basket").val());
        }, 1000);
        $.get($(".basket-url").val(), function (data) {
          // Выбор контейнера на другой странице, куда будет отображено содержимое
          let container = $(".modal-basket");
          // Вставка полученного HTML-содержимого в контейнер
          container.html(data);
        });

        $.ajax({
          type: 'GET',
          url: updater_url,
          success: (response) => {
            $('.products_amount').html(response.count_product)
          }
        })
      },
    });
  });

  // ----------------modal-basket----------------//

  // Выполнение асинхронного запроса на сервер для получения HTML-страницы
  $.get($(".basket-url").val(), function (data) {
    // Выбор контейнера на другой странице, куда будет отображено содержимое
    let container = $(".modal-basket");
    // Вставка полученного HTML-содержимого в контейнер
    container.html(data);
  });

  $(".basket_btn").click(function () {
    $(".modal-basket").css("display", "flex");
    $("body").css("overflow", "hidden");
    $(".modal-basket-cloth").css("display", "flex");
  });

  $.get($(".profile-url").val(), function (data) {
    // Выбор контейнера на другой странице, куда будет отображено содержимое
    let container = $(".modal-profile");
    // Вставка полученного HTML-содержимого в контейнер
    container.html(data);
  });

  $(".profile_btn").click(function () {
    $(".modal-profile").css("display", "flex");
    $("body").css("overflow", "hidden");
    $(".modal-basket-cloth").css("display", "flex");
  });

  $(".profile_burger_btn").click(function () {
    $(".modal-profile").css("display", "flex");
    $("body").css("overflow", "hidden");
    $(".modal-basket-cloth").css("display", "flex");
  });
});
