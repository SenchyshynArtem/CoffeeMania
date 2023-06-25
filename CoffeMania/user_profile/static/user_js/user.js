$(document).ready(function () {
  $(".close_profile").click(function () {
    $(".modal-profile").css("display", "none");
    $("body").css("overflow", "auto");
    $(".modal-basket-cloth").css("display", "none");
    $("body").css("overflow-x", "hidden");
  });

  $(".modal-basket-cloth").click(function () {
    $(".modal-profile").css("display", "none");
    $("body").css("overflow", "auto");
    $(".modal-basket-cloth").css("display", "none");
    $("body").css("overflow-x", "hidden");
  });

  $(".my_profile").click(function () {
    $(".profile_setting").css("display", "none");
    // $(".settings_profile").css("background", "#9afbb5");
    $(".my_profile").css("background", "#85DB9D");
    $(".profile_page").css("display", "flex");
  });

  $(".edit_form").on("click", ".edit_icon", function () {
    $(this).parent().find("input").prop("readonly", false);
    $(this).parent().find("input").css("border", "2px solid white");
    $(this).parent().find("input").focus();
    $(this).parent().find("input").select();
    $(this).attr("src", $(".swap_confirm_edit").val());
    $(this).addClass("send_change");
    $(this).removeClass("edit_icon");
  });

  $(".edit_form").on("click", ".send_change", function () {
    const button_this = $(this);
    $.ajax({
      type: "POST",
      url: $(".url_for_swap").val(),
      data: $(".edit_form").serializeArray(),
      success: () => {
        button_this.parent().find("input").prop("readonly", true);
        button_this.parent().find("input").css("border", "none");
        button_this.attr("src", $(".swap_edit_icon").val());
        button_this.addClass("edit_icon");
        button_this.removeClass("send_change");
      },
    });
  });
});

// $(".settings_profile").click(function () {
//   $(".profile_page").css("display", "none");
//   $(".my_profile").css("background", "#9afbb5");
//   $(".settings_profile").css("background", "#85DB9D");
//   $(".profile_setting").css("display", "flex");
// });
