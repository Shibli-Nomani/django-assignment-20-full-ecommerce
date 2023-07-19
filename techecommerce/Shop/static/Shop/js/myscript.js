// Initiate the wowjs
//new WOW().init();


//owl-carousel

$('.slider1').owlCarousel({
      loop:true,
      margin:10,
      nav:true,
      dots:true,
      autoplay:true,
      autoplayHoverPause:true,
      navText: ["<img src='https://freepngimg.com/thumb/arrow/163768-arrow-left-free-photo.png' id='pre-left'>", "<img src='https://www.freeiconspng.com/thumbs/arrow-icon/right-arrow-icon-27.png' id='next-right'>" ],
      responsive:{
        
          480:{
      items:2
        },
          768 :{
      items:1
        }
      }
  
});

//3 items
$(".slider3").owlCarousel({
  loop: true,
  margin: 20,
  responsiveClass: true,
  navText: ["<img src='https://freepngimg.com/thumb/arrow/163768-arrow-left-free-photo.png' id='pre-left-pro'>", "<img src='https://www.freeiconspng.com/thumbs/arrow-icon/right-arrow-icon-27.png' id='next-right-pro'>" ],
  responsive: {
    
    600: {
      items: 3,
      nav: true,
      autoplay: true,
    }
  }
});

//4 items
$(".slider4").owlCarousel({
  loop: true,
  margin: 20,
  responsiveClass: true,
  navText: ["<img src='https://freepngimg.com/thumb/arrow/163768-arrow-left-free-photo.png' id='pre-left-pro'>", "<img src='https://www.freeiconspng.com/thumbs/arrow-icon/right-arrow-icon-27.png' id='next-right-pro'>" ],
  responsive: {
    800: {
      items: 4,
      nav: true,
      autoplay: true,
    }
  }
});






//cart plus
/* plus-cart define in html as class */
$(".plus-cart").click(function () {
  /*this: current pid stores into var id as string*/
  var id = $(this).attr("pid").toString();
  var eml = this.parentNode.children[2];
  // console.log(id);
  $.ajax({
    
    type: "GET",
    /* url as per urls.py */
    url: "/pluscart",
    data: {
      /*data coming from product id*/
      /*prod_id declares in views.py also*/
      prod_id: id,
    },
    /*data: coming from views.py and attributes also*/
    /* must call all attributes under data(which is coming from views.py) */
    success: function (data) {
      eml.innerText = data.quantity;
      document.getElementById("amount").innerText = data.amount;
      document.getElementById("shipping_amount").innerText = data.shipping_amount;
      document.getElementById("totalamount").innerText = data.totalamount;
    },
  });
});

//cart minus
/* minus-cart define in html as class */
$(".minus-cart").click(function () {
  var id = $(this).attr("pid").toString();
  var eml = this.parentNode.children[2];
  // console.log(id);
  $.ajax({
    type: "GET",
    url: "/minuscart",
    data: {
      prod_id: id,
    },

    /*data: coming from views.py and attributes also*/
    /* must call all attributes under data(which is coming from views.py) */
    success: function (data) {
      eml.innerText = data.quantity;
      document.getElementById("amount").innerText = data.amount;
      document.getElementById("shipping_amount").innerText = data.shipping_amount;
      document.getElementById("totalamount").innerText = data.totalamount;
    },
  });
});

//Remove item from cart 
$(".remove-item").click(function () {
  var id = $(this).attr("pid").toString();
  var eml = this;
  // console.log(id);
  $.ajax({
    type: "GET",
    url: "/removeitem",
    data: {
      prod_id: id,
    },
    /* must call all attributes under data(which is coming from views.py) */
    success: function (data) {
      document.getElementById("amount").innerText = data.amount;
      document.getElementById("shipping_amount").innerText = data.shipping_amount;
      document.getElementById("totalamount").innerText = data.totalamount;
      /* here four nodes(product_image, title, discription, quantity) are connected in shopping cart item*/
      eml.parentNode.parentNode.parentNode.parentNode.remove();
    },
  });
});

//payment done
