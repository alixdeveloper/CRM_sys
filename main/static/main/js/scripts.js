var checkbox = document.querySelector('.theme-switch__checkbox');

checkbox.addEventListener('change', function () {
    transition();

    if (this.checked) {
        var theme = "dark";

    } else {
        var theme = 'light';

    }
    $.ajax({
        type: 'POST',
        url: "/status",
        data: {csrfmiddlewaretoken: window.CSRF_TOKEN, theme: theme},
        success: function (data) {
            if (theme == 'dark') {
                document.documentElement.setAttribute('data-theme', 'dark');
            } else {
                document.documentElement.setAttribute('data-theme', 'light');
            }
        }
    })

})

function transition() {
    document.documentElement.classList.add('transition');
    setTimeout(function () {
        document.documentElement.classList.remove('transition');
    }, 2500)
}
 $.ajax({
    type: 'GET',
    url: "/status",
    data: {csrfmiddlewaretoken: window.CSRF_TOKEN},
    success: function (data) {
        if (data == 'dark') {
            document.documentElement.setAttribute('data-theme', 'dark');
        } else {
            document.documentElement.setAttribute('data-theme', 'light');
        }
    }
})



                document.querySelectorAll('.table-scroll-vertical').forEach(item => {
                        item.scrollTop = item.scrollHeight;

                })





            document.querySelectorAll('.close_payment').forEach(item => {
            item.addEventListener('click', event => {

                swal({
                     title: "Подтверждение",
  text: "Операция: Удаление платежа\n"+ "Название: "+'"'+item.children[0].innerText+'"',
  icon: "warning",
  buttons: ["Отмена", "Ок"],

                }).then((willDelete) => {
                      if (willDelete) {


                $.ajax({
                    type: 'POST',
                    url: '/delete',
                    data: {
                        data_id: $(item).attr('name'),
                        data_type: 'payment',
                        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                        action: 'post'
                    },
                    beforeSend: function () {

                        // $(item).hide(250);
                    },
                    success: function (json) {
                        $(item).find('td').text('Удалено');

                        if (!$('#payment_table tbody .close_payment').length){
                            $('#payment_table .data_table').hide(250);
                        }
                        location.reload();


                    },
                    error: function (xhr, errmsg, err) {
                        $('#' + $(item).attr('name')).find('td').text('Ошибка! Можешь попробавть ещё...');

                        $(item).show(250);

                        $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                            " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                    }

                });
                          }else {
                          null
                      }})
            });
        });


        document.querySelectorAll('.dropdown-status').forEach(item => {
            item.addEventListener('click', event => {
                                            $.ajax({
                                type: 'POST',
                                url: '/change_product_status',
                                data: {
                                    data_id: $(item).attr('product_id'),
                                    new_status: item.innerHTML,
                                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                                    action: 'post',

                                },
                                beforeSend: function () {

                                    // $(item).hide(250);
                                },
                                success: function (json) {
                                    $('#' + $(item).attr('name')).find('td').text('Удалено');
                                    var button = document.getElementById('button'+$(item).attr('product_id'));
                                    button.innerHTML = item.innerHTML;
                                    location.reload();
                                },
                                error: function (xhr, errmsg, err) {
                                    // $('#' + $(item).attr('name')).find('td').text('Ошибка! Можешь попробавть ещё...');

                                    // $(item).show(250);

                                    // $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                                    //     " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                                    // console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                                }

                            });

            })
        })
        document.querySelectorAll('.dropdown-order').forEach(item => {
            item.addEventListener('click', event => {
                                            $.ajax({
                                type: 'POST',
                                url: '/change_product_order',
                                data: {
                                    data_id: $(item).attr('product_id'),
                                    new_order: $(item).attr('order_id'),
                                    old_order:  $(item).attr('old_order'),
                                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                                    action: 'post',

                                },
                                beforeSend: function () {
                                    // $(item).hide(250);
                                },
                                success: function (json) {
                                    $('#' + $(item).attr('name')).find('td').text('Удалено');
                                    var button = document.getElementById('button'+$(item).attr('product_id'));
                                    button.innerHTML = item.innerHTML;
                                    window.location.replace('/order/'+json.order+'/?product='+json.product)

                                },
                                error: function (xhr, errmsg, err) {

                                    // $('#' + $(item).attr('name')).find('td').text('Ошибка! Можешь попробавть ещё...');

                                    // $(item).show(250);

                                    // $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                                    //     " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                                    // console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                                }

                            });

            })
        })
        document.querySelectorAll('.product-image').forEach(item => {
            item.addEventListener('click', event => {

                swal({
  title: "Подтверждение",

  text: "Удаляем фото!",

  icon: "warning",
  buttons: ["Отмена", "Ок"],
})
.then((willDelete) => {
  if (willDelete) {
      $.ajax({
          type: 'POST',
          url: '/delete',
          data: {
              data_id: $(item).attr('product_id'),
              photo_id: $(item).attr('filename'),
              data_type: 'photo',
              csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
              action: 'post',

          },
          beforeSend: function () {

              // $(item).hide(250);
          },
          success: function (json) {
              $(item).hide(200);
location.reload();
          },
          error: function (xhr, errmsg, err) {
              // $('#' + $(item).attr('name')).find('td').text('Ошибка! Можешь попробавть ещё...');

              // $(item).show(250);

              // $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
              //     " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
              // console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
          }

      });
  }})
            })
        })
                    document.querySelectorAll('.pay_info').forEach(item => {
                item.addEventListener('click', event => {

                });
            });

   function truncated(num) {
        return Math.trunc(num * 100) / 100;
    }

    function calculate_price0(source) {
        var client_price = document.getElementById("client_price"+source);
        var one = document.getElementById("one"+source);
        var two = document.getElementById("two"+source);
        var price = document.getElementById("price"+source);
        if (price.value.substr(0, 1) == '0') price.value = price.value.substr(1);

        if (one.value == '') one.value = 0;
        if (client_price.value == '') client_price.value = 0;
        if (two.value == '') two.value = 0;
        if (price.value == '') price.value = 0;
        client_price.value = parseFloat(price.value) + parseFloat(one.value);
        two.value = parseFloat(one.value) / (parseFloat(price.value) / 100);


    }

    function calculate_price1(source) {
        var one = document.getElementById("one"+source);
        var two = document.getElementById("two"+source);
        var client_price = document.getElementById("client_price"+source);
        var price = document.getElementById("price"+source);
        if (one.value.substr(0, 1) == '0') one.value = one.value.substr(1);

        if (one.value == '') one.value = 0;
        if (price.value == '') price.value = 0;

        two.value = parseFloat(one.value) / (parseFloat(price.value) / 100);
        client_price.value = parseFloat(price.value) + parseFloat(one.value);
        // one.value = (parseFloat(price.value)/100)*parseFloat(two.value);

    }

    function calculate_price2(source) {
        var one = document.getElementById("one"+source);
        var two = document.getElementById("two"+source);
        var client_price = document.getElementById("client_price"+source);
        var price = document.getElementById("price"+source);
        if (two.value.substr(0, 1) == '0') two.value = two.value.substr(1);

        if (one.value == '') one.value = 0;
        if (two.value == '') two.value = 0;
        if (price.value == '') price.value = 0;

        one.value = (parseFloat(price.value) / 100) * parseFloat(two.value);
        client_price.value = parseFloat(price.value) + parseFloat(one.value);
        // two.value = parseFloat(one.value)/(parseFloat(price.value)/100);


    }

    function calculate_price3(source) {
        var one = document.getElementById("one"+source);
        var two = document.getElementById("two"+source);
        var client_price = document.getElementById("client_price"+source);
        var price = document.getElementById("price"+source);
        if (client_price.value.substr(0, 1) == '0') client_price.value = client_price.value.substr(1);

        if (one.value == '') one.value = 0;
        if (client_price.value == '') client_price.value = 0;
        if (price.value == '') price.value = 0;

        one.value = parseFloat(client_price.value) - parseFloat(price.value);
        two.value = parseFloat(one.value) / (parseFloat(price.value) / 100);

    }


    var timer_id = 0; //глобальная переменная, хранящая ID таймера
    var menu = false; //переменная, хранящая информацию о том, отработал ли длинный клик
    $(".product-data").focusout(function () {

    var el_product = $(this);
    var name = $('[name="product_name_'+el_product.attr("product_id")+'"]');
    var material = $('[name="product_material_'+el_product.attr("product_id")+'"]');
    var category = $('[name="category_'+el_product.attr("product_id")+'"]');
    var create_date = $('[name="create_date_product_'+el_product.attr("product_id")+'"]');
    var complete_date = $('[name="complete_date_product_'+el_product.attr("product_id")+'"]');
    var preorder_weight_product = $('[name="preorder_weight_product_'+el_product.attr("product_id")+'"]');
    if (preorder_weight_product.val()){
        preorder_weight_product = preorder_weight_product.val()
    }
    else{
        preorder_weight_product = 0;
    }
    var color = $('[name="product_color_'+el_product.attr("product_id")+'"]');
    var weight =  $('[name="product_weight_'+el_product.attr("product_id")+'"]');
    var length =  $('[name="product_length_'+el_product.attr("product_id")+'"]');
    var width =  $('[name="product_width_'+el_product.attr("product_id")+'"]');
    var height =  $('[name="product_height_'+el_product.attr("product_id")+'"]');
    var psize =  $('[name="product_size_'+el_product.attr("product_id")+'"]');
    var product_id = el_product.attr('product_id');
    if (el_product.val() != el_product.attr('value')){
        swal({
  title: "Подтверждение",

  text: "Изменяем поле "+ '"'+el_product.attr('label')+'"'+ "\n"+"Было: "+el_product.attr('value')+"\n"+"Стало: "+el_product.val(),

  icon: "warning",
  buttons: ["Отмена", "Ок"],
})
.then((willDelete) => {
  if (willDelete) {
$.ajax({
                type: 'POST',
                url: '/change_product_info',
                data: {
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                    action: 'post',
                    product_id: product_id,
                    psize: psize.val(),
                    height: height.val(),
                    category: category.val(),
                    create_date: create_date.val(),
                    complete_date: complete_date.val(),
                    preorder_weight_product: preorder_weight_product,
                    width: width.val(),
                    length: length.val(),
                    weight: weight.val(),
                    color: color.val(),
                    material: material.val(),
                    name: name.val(),
                    prev: el_product.attr('value'),
                    new: el_product.val(),
                    label: el_product.attr('label'),
                    place: "Изделие",
                    identification: el_product.attr('product_id'),

                },
                beforeSend: function () {
                     },
                success: function (json) {
                    //swal("Готово", "Изменения были сохранены", "success",{buttons: [, '✔']});
                    swal("Готово", "Изменения были сохранены", "success",{buttons: false, timer: 1300,});

                    el_product.attr("value",el_product.val());
location.reload();

                },
                error: function (xhr, errmsg, err) {
                    swal("Всё плохо!","Что-то пошло не так и изменения не были сохранены!");
                    el_product.val(el_product.attr("value"));

                }

            });

  } else {
    el_product.val(el_product.attr('value'));
  }
});
}
    else {

    }
    });




    $(".client-data").focusout(function () {
    var el_client = $(this);
    var last_name = $('[name="last_name"][client_id="'+el_client.attr('client_id')+'"]');
    var first_name = $('[name="first_name"][client_id="'+el_client.attr('client_id')+'"]');
    var middle_name = $('[name="middle_name"][client_id="'+el_client.attr('client_id')+'"]');
    var phone =  $('[name="phone"][client_id="'+el_client.attr('client_id')+'"]');
    var city =  $('[name="city"][client_id="'+el_client.attr('client_id')+'"]');
    var communication_type =  $( "#communication_type");
    var client_id = el_client.attr('client_id');
    if (el_client.val() != el_client.attr('value') || $( "#communication_type option:selected").val()!=communication_type.val()){
        swal({
  title: "Подтверждение",

  text: "Изменяем поле "+ '"'+el_client.attr('label')+'"'+ "\n"+"Было: "+el_client.attr('value')+"\n"+"Стало: "+el_client.val(),

  icon: "warning",
  buttons: ["Отмена", "Ок"],
})
.then((willDelete) => {
  if (willDelete) {
$.ajax({
                type: 'POST',
                url: '/change_client_info',
                data: {
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                    action: 'post',
                    client_id: client_id,
                    last_name: last_name.val(),
                    first_name: first_name.val(),
                    middle_name: middle_name.val(),
                    phone: phone.val(),
                    city: city.val(),
                    communication_type: $("[name=communication_type][client_id="+el_client.attr('client_id')+"]").val(),
                    prev: el_client.attr('value'),
                    new: el_client.val(),
                    label: el_client.attr('label'),
                    place: "Клиент",
                    identification: el_client.attr('client_id'),

                },
                beforeSend: function () {
                     },
                success: function (json) {
                    //swal("Готово", "Изменения были сохранены", "success",{buttons: [, '✔']});
                    swal("Готово", "Изменения были сохранены", "success",{buttons: false, timer: 1300,});
                    $('[client_id='+el_client.attr("client_id")+'] a').attr('href', 'tel:'+$('[client_id='+el_client.attr("client_id")+'] [name="phone"]').val());
                    el_client.attr("value",el_client.val());
location.reload();

                },
                error: function (xhr, errmsg, err) {
                    swal("Всё плохо!","Что-то пошло не так и изменения не были сохранены!");
                    el_client.val(el_client.attr("value"));

                }

            });

  } else {
    el_client.val(el_client.attr('value'));
  }
});
}
    else {

    }
    });




    var timer_id = 0; //глобальная переменная, хранящая ID таймера
    var menu = false; //переменная, хранящая информацию о том, отработал ли длинный клик
    $(".order-data").focusout(function () {

    var el = $(this);
    var name = $('[name="name"]');
    var create_date = $('[name="create_date"]');
    var complete_date = $('[name="complete_date"]');
    var weight =  $('[name="weight"]');
    var price =  $('[name="price"]');
    var prepayment =  $('[name="prepayment"]');
    var preorder_weight = $('[name="preorder_weight"]');
    var ads = $('[name="ads"]');
    if (el.val() != el.attr('value')){
        swal({
  title: "Подтверждение",
  text: "Изменяем поле "+ '"'+el.attr('content')+'"'+ "\n"+"Было: "+ el.attr('value') +"\n"+"Стало: "+el.val(),
  icon: "warning",
  buttons: ["Отмена", "Ок"],
})
.then((willDelete) => {
  if (willDelete) {
$.ajax({
                type: 'POST',
                url: '/change_order_info',
                data: {
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                    action: 'post',
                    name: name.val(),
                    create_date: create_date.val(),
                    complete_date: complete_date.val(),
                    weight: weight.val(),
                    price: price.val(),
                    prepayment: prepayment.val(),
                    preorder_weight: preorder_weight.val(),
                    ads: ads.val(),
                    prev: el.attr('value'),
                    new: el.val(),
                    label: el.attr('content'),
                    place: "Заказ",
                    identification: "{{ order.id }}",
                },
                beforeSend: function () {
                     },
                success: function (json) {
                    //swal("Готово", "Изменения были сохранены", "success",{buttons: [, '✔']});
                    swal("Готово", "Изменения были сохранены", "success",{buttons: false, timer: 1300,});
                    el.attr("value",el.val());
location.reload();

                },
                error: function (xhr, errmsg, err) {
                    swal("Всё плохо!","Что-то пошло не так и изменения не были сохранены!");
                    el.val(el.attr("value"));

                }

            });

  } else {
    el.val(el.attr('value'));
  }
});
}
    else {

    }
    });




    // $("#weight").mousedown(function () {
    //     timer_id = setTimeout('showMenu()', 1000)
    // });
    // $("#weight").mouseup(function () {
    //     clearTimeout(timer_id);
    //     if (!menu) fastClick();
    // });

    //Функция, которая отрабатывает при длинном клике
    function showMenu() {
        menu = true;
        alert('длинный');
    }

    //Функция, которая отрабатывает при коротком клике
    function fastClick() {
        alert('короткий');
    }
    var timer_id = 0; //глобальная переменная, хранящая ID таймера
    var menu = false; //переменная, хранящая информацию о том, отработал ли длинный клик
    $(".order-data").focusout(function () {

    var el = $(this);
    var name = $('[name="name"]');
    var create_date = $('[name="create_date"]');
    // var complete_date = $('[name="complete_date"]');
    var weight =  $('[name="weight"]');
    // var price =  $('[name="price"]');
    // var prepayment =  $('[name="prepayment"]');
    // var preorder_weight = $('[name="preorder_weight"]');
    var ads = $('[name="ads"]');
    if (el.val() != el.attr('value')){
        swal({
  title: "Подтверждение",
  text: "Изменяем поле "+ '"'+el.attr('content')+'"'+ "\n"+"Было: "+ el.attr('value') +"\n"+"Стало: "+el.val(),
  icon: "warning",
  buttons: ["Отмена", "Ок"],
})
.then((willDelete) => {
  if (willDelete) {
$.ajax({
                type: 'POST',
                url: '/change_order_info',
                data: {
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                    action: 'post',
                    name: name.val(),
                    create_date: create_date.val(),
                    // complete_date: complete_date.val(),
                    weight: weight.val(),
                    // price: price.val(),
                    // prepayment: prepayment.val(),
                    // preorder_weight: preorder_weight.val(),
                    ads: ads.val(),
                    prev: el.attr('value'),
                    new: el.val(),
                    label: el.attr('content'),

                    place: "Заказ",
                    identification: "{{ order.id }}",
                },
                beforeSend: function () {
                     },
                success: function (json) {
                    //swal("Готово", "Изменения были сохранены", "success",{buttons: [, '✔']});
                    swal("Готово", "Изменения были сохранены", "success",{buttons: false, timer: 1300,});
                    el.attr("value",el.val());
location.reload();

                },
                error: function (xhr, errmsg, err) {
                    swal("Всё плохо!","Что-то пошло не так и изменения не были сохранены!");
                    el.val(el.attr("value"));

                }

            });

  } else {
    el.val(el.attr('value'));
  }
});
}
    else {

    }
    });




    // $("#weight").mousedown(function () {
    //     timer_id = setTimeout('showMenu()', 1000)
    // });
    // $("#weight").mouseup(function () {
    //     clearTimeout(timer_id);
    //     if (!menu) fastClick();
    // });

    //Функция, которая отрабатывает при длинном клике
    function showMenu() {
        menu = true;
        alert('длинный');
    }

    //Функция, которая отрабатывает при коротком клике
    function fastClick() {
        alert('короткий');
    }



    var mprice = document.getElementById('price');

    document.querySelectorAll('.calc').forEach(item => {
        item.addEventListener('focus', event => {
            var price = document.getElementById('price'+item.getAttribute('source'));
            if (price.value.length == 0 || price.value == 0) {
                price.focus();
            }
        })
    })


    function payment_control(val, source) {
        var count = document.getElementById('count'+source);
        var finance_desc = document.getElementById('finance_desc'+source);
        var price = document.getElementById('price'+source);
        var content_calc = document.getElementById('content_calc'+source);
        var description = document.getElementById('description'+source);
        if (val === 'dohod') {
            count.innerText = 'Сумма';
            finance_desc.style.display = '';
            if (content_calc) {

                content_calc.remove();
            }
            description.setAttribute('placeholder', 'Комментарий');
            price.setAttribute('placeholder', 'Сколько денег получено');
        } else if (val === 'rashod') {
            finance_desc.style.display = '';
            count.innerText = 'Себестоимость';
            price.setAttribute('placeholder', 'Сколько денег потрачено');
            var newTr = document.createElement("tr");
            description.setAttribute('placeholder', 'Комментарий расхода');

            newTr.innerHTML = "<td >Наценка<input id=\"one"+source+"\"  class=\"form-control calc\" value=\"\" onkeyup=\"calculate_price1(\'"+source+"\')\" type=\"number\" placeholder=\"Наценка\"></td>\n" +
                "                            <td>Наценка %<input   onkeyup=\"calculate_price2(\'"+source+"\')\" id=\"two"+source+"\" class=\"form-control calc\" value=\"\" type=\"number\" value=\"any\" placeholder=\"От моей цены\"></td>\n" +
                "                            <td>Цена клиента<input value=\"0\" onkeyup=\"calculate_price3(\'"+source+"\')\" id=\"client_price"+source+"\" class=\"form-control calc\" type=\"number\" required placeholder=\"Цена клиента\"></td>";
            newTr.id = 'content_calc'+source;
            var first = document.getElementById('first'+source);
            first.parentNode.insertBefore(newTr, first.nextElementSibling);
            var price = document.getElementById('price'+source);

            document.querySelectorAll('.calc'+source).forEach(item => {
                item.addEventListener('focus', event => {
                    if (price.value.length == 0) {
                        price.focus();
                    }
                })
            })

        }
        else if (val === 'rabota') {
            finance_desc.style.display = '';

            count.innerText = 'Стоимость';
            if (content_calc) {
                content_calc.remove();
            }
            description.setAttribute('placeholder', 'Описание работы');
            price.setAttribute('placeholder', 'Стоимость работы');

        }
        else if (val === 'predoplata') {
            finance_desc.style.display = 'none';

            count.innerText = 'Стоимость';
            if (content_calc) {
                content_calc.remove();
            }
            description.setAttribute('placeholder', 'Описание работы');
            price.setAttribute('placeholder', 'Стоимость работы');

        }
    }



    document.querySelectorAll('.new_comment_order').forEach(item => {
                        item.addEventListener('click', event => {
                        if ($('#comment_order').val() != ''){
                        $.ajax({
                                type: 'POST',
                                url: '/create_comment_order',
                                data: {
                                    comment: $('#comment_order').val(),
                                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                                    action: 'post'
                                },
                                beforeSend: function () {
                                    $('#spinner_order').attr('style', 'display:inline');
                                    $('#comment_label_order').attr('style', 'display:none');
                                },
                                success: function (json) {
                                    $('#empty_label_comment_order').remove();

                                    $('#spinner_order').attr('style', 'display:none');
                                    $('#comment_label_order').attr('style', 'display:inline');
                                    $('#comment_order').val('');
                                    $('#data_of_comments_order').append(
                                        '<tr id=' + json.id + '><th scope="row">' + json.date + '</th><td style="word-wrap: break-word;">' + json.message + '<button type="button" style="display:inline" class="close close_comment" name="' + json.id + '" aria-label="Close"><span aria-hidden="true">&times;</span></button></td></tr>'
                                    );
                                    document.querySelectorAll('.close_comment').forEach(item => {
                                        item.addEventListener('click', event => {
                                            $.ajax({
                                                type: 'POST',
                                                url: '/delete',
                                                data: {
                                                    data_id: $(item).attr('name'),
                                                    data_type: 'comment',
                                                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                                                    action: 'post'
                                                },
                                                beforeSend: function () {

                                                    $(item).hide(250);
                                                },
                                                success: function (json) {
                                                    $('#' + $(item).attr('name')).find('td').text('Удалено');

                                                },
                                                error: function (xhr, errmsg, err) {
                                                    $('#' + $(item).attr('name')).find('td').text('Ошибка! Можешь попробавть ещё...');

                                                    $(item).show(250);

                                                    $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                                                        " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                                                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                                                }

                                            });
                                        });
                                    });
                                                    document.querySelectorAll('.table-scroll-vertical').forEach(item => {
                        item.scrollTop = item.scrollHeight;

                })




                                },
                                error: function (xhr, errmsg, err) {
                                    $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                                        " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                                }

                            });
                            }
                        else{
                            $('#comment_order').val('');

                        }
                        })
                                            document.querySelectorAll('.close_comment').forEach(item => {
                                        item.addEventListener('click', event => {
                                            $.ajax({
                                                type: 'POST',
                                                url: '/delete',
                                                data: {
                                                    data_id: $(item).attr('name'),
                                                    data_type: 'comment',
                                                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                                                    action: 'post'
                                                },
                                                beforeSend: function () {

                                                    $(item).hide(250);
                                                },
                                                success: function (json) {
                                                    $('#' + $(item).attr('name')).find('td').text('Удалено');

                                                },
                                                error: function (xhr, errmsg, err) {
                                                    $('#' + $(item).attr('name')).find('td').text('Ошибка! Можешь попробавть ещё...');

                                                    $(item).show(250);

                                                    $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                                                        " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                                                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                                                }

                                            });
                                        });
                                    });


            ;
        });
    document.querySelectorAll('.new_comment_product').forEach(item => {
                        item.addEventListener('click', event => {
if ($('#comment_product'+item.getAttribute('product_id')).val() != '') {
    $.ajax({
        type: 'POST',
        url: '/create_comment_product',
        data: {
            comment: $('.comment_product_text[product_id=' + item.getAttribute("product_id") + ']').val(),
            product_id: item.getAttribute('product_id'),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            action: 'post'
        },
        beforeSend: function () {
            $('#spinner_product' + item.getAttribute("product_id")).attr('style', 'display:inline');
            $('#comment_label_product' + item.getAttribute("product_id")).attr('style', 'display:none');
        },
        success: function (json) {
            $('#empty_label_comment_product' + item.getAttribute("product_id")).remove();

            $('#spinner_product' + item.getAttribute("product_id")).attr('style', 'display:none');
            $('#comment_label_product' + item.getAttribute("product_id")).attr('style', 'display:inline');
            $('#comment_product' + item.getAttribute("product_id")).val('');
            $('#data_of_comments_product' + item.getAttribute("product_id")).append(
                '<tr id=' + json.id + '><th scope="row">' + json.date + '</th><td style="word-wrap: break-word;">' + json.message + '<button type="button" style="display:inline" class="close close_comment" name="' + json.id + '" aria-label="Close"><span aria-hidden="true">&times;</span></button></td></tr>'
            );
            document.querySelectorAll('.close_comment').forEach(item => {
                item.addEventListener('click', event => {
                    $.ajax({
                        type: 'POST',
                        url: '/delete',
                        data: {
                            data_id: $(item).attr('name'),
                            data_type: 'comment',
                            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                            action: 'post'
                        },
                        beforeSend: function () {

                            $(item).hide(250);
                        },
                        success: function (json) {
                            $('#' + $(item).attr('name')).find('td').text('Удалено');

                        },
                        error: function (xhr, errmsg, err) {
                            $('#' + $(item).attr('name')).find('td').text('Ошибка! Можешь попробавть ещё...');

                            $(item).show(250);

                            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                        }

                    });
                });
            });
            document.querySelectorAll('.table-scroll-vertical').forEach(item => {
                item.scrollTop = item.scrollHeight;

            })


        },
        error: function (xhr, errmsg, err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }

    });
}


        });

;})




    var queryString = window.location.search;

    var urlParams = new URLSearchParams(queryString);

    var product = urlParams.get('product')
    if (product) {
        product_place = $('a[href="#product' + product + '"]');

        //calculate destination place
        var dest = 0;
        dest = product_place.offset().top;

        //go to destination
        $('html,body').animate({scrollTop: dest}, 1000, 'swing', function () {
product_place.click();
        });


    }
