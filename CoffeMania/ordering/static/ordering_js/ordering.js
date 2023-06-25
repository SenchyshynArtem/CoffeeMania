$(document).ready(function () {
    $("#phone").inputmask("+(380) 99-999-9999");
  
    $("#street").on("input", function () {
        var inputValue = $(this).val();
        var reg = /^[a-zA-Zа-яА-ЯіІїЇєЄёЁ\s]+$/u;
      
        if (!reg.test(inputValue)) {
          $(this).val(inputValue.replace(/[^a-zA-Zа-яА-ЯіІїЇєЄёЁ\s]/ug, ""));
        }
      });
      
  
    $("#build, #room").on("input", function () {
      var inputValue = $(this).val();
      var reg = /^\d*$/;
  
      if (!reg.test(inputValue)) {
        $(this).val(inputValue.replace(/\D/g, ""));
      }
    });
  
    // Валидация формы перед отправкой
    $("form").submit(function (event) {
      event.preventDefault();
      var isValid = true;
      $(".form-group").removeClass("error");
      $(".form-group .error-message").text("");
      let redirect_url = $('.redirect_url').val()
  
      // Проверка заполненности полей
      $(".form-group input").each(function () {
        var value = $(this).val().trim();
        if (value === "") {
          var fieldName = $(this).attr("name");
          var errorMessage =
            "Поле '" + fieldName + "' обов'язкове для заповнення";
          $(this).closest(".form-group").addClass("error");
          $(this).siblings(".error-message").text(errorMessage);
          isValid = false;
        }
      });
      
      if (isValid) {
        let url = $(".url").val();
        let data = $(this).serializeArray();
        $.ajax({
          type: "POST",
          url: url,
          data: data,
          success: () => {
            window.location = redirect_url
          },
        });
      }
    });
  });
  