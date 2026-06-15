(function ($) {
    "use strict";
    // scroll to top section
    $(function () {
        const $btn = $(".scroll-to-top-button").hide();
        $(window).on("scroll", function () {
            $btn.toggle($(this).scrollTop() > 100);
        });
        $btn.on("click", function (e) {
            e.preventDefault();
            $("html, body").animate({ scrollTop: 0 }, 600);
        });
    });
    // custom cursor section
    $(function () {
        const $c = $(".cursor");
        let mx = 0, my = 0, x = 0, y = 0;
        $(document).on("mousemove", function (e) {
            mx = e.clientX;
            my = e.clientY;
            $c.toggleClass("hover", $(e.target).css("cursor") === "pointer");
        });
        (function anim() {
            x += (mx - x) * 0.15;
            y += (my - y) * 0.15;
            $c.css({ left: x, top: y });
            requestAnimationFrame(anim);
        })();
    });
    // AOS animation
    $(function () {
        setTimeout(() => AOS.init({ once: false, mirror: true }), 500);
    });
    // preloader section
    $(window).on("load", function () {
        $("#preloader").css("opacity", 0).on("transitionend", function () {
            $(this).hide();
        });
    });
    // make sticky navbar
    $(function () {
        const $navbar = $(".top-navbar");
        $(window).on("scroll", function () {
            $navbar.toggleClass("sticky", $(this).scrollTop() > 100);
        });
    });
    // header section
    $(function () {
        const page = location.pathname.split("/").pop() || "index.html",
            norm = h => (h || "").replace("./", "").split("/").pop(),
            $nav = $(".mobile-nav"), $overlay = $(".menu-overlay");
        $(".active-link, .active-mid, .active-sub").removeClass("active-link active-mid active-sub");
        $(".dropdown").each(function () {
            const $drop = $(this), $parentA = $drop.children("a");
            if (norm($parentA.attr("href")) === page) {
                $drop.addClass("active-link");
                return;
            }
            $drop.find(".submenu-right a").each(function () {
                if (norm(this.href) === page) {
                    $drop.addClass("active-link");
                    $(this).closest(".dropdown-sub").addClass("active-mid");
                    $(this).parent().addClass("active-sub");
                }
            });
            $drop.find("> .submenu a").each(function () {
                if (norm(this.href) === page) {
                    $drop.addClass("active-link");
                    $(this).parent().addClass("active-sub");
                }
            });
        });
        $("li:not(.dropdown) > a").each(function () {
            if (norm(this.href) === page) {
                $(this).parent().addClass("active-link");
            }
        });
        const openMenu = () => {
            $nav.addClass("active");
            $overlay.addClass("active");
            if (innerWidth <= 1199) {
                $(".active-link > .submenu").addClass("open");
                $(".active-mid > .submenu-right").addClass("open");
            }
        };
        const closeMenu = () => {
            $nav.removeClass("active");
            $overlay.removeClass("active");
            $(".submenu.open, .submenu-right.open").removeClass("open");
        };
        $(document).on("click", function (e) {
            const $t = $(e.target);
            if ($t.closest(".menu-toggle").length) {
                $nav.hasClass("active") ? closeMenu() : openMenu();
                return;
            }
            if ($t.closest(".close-icon, .menu-overlay").length) {
                closeMenu();
                return;
            }
            if (innerWidth > 1199) return;
            const $main = $t.closest(".dropdown > a");
            if ($main.length) {
                const $sub = $main.next(".submenu");
                if ($sub.length) {
                    e.preventDefault();
                    $(".submenu.open").not($sub).removeClass("open");
                    $sub.toggleClass("open");
                }
                return;
            }
            const $subLink = $t.closest(".dropdown-sub > a");
            if ($subLink.length) {
                const $sub = $subLink.next(".submenu-right");
                if ($sub.length) {
                    e.preventDefault();
                    $(".submenu-right.open").not($sub).removeClass("open");
                    $sub.toggleClass("open");
                }
            }
        });
    });
    // service solutions section
    $(function () {
        $(".service-solutions-autoplay").slick({
            variableWidth: true,
            slidesToShow: 4,
            slidesToScroll: 1,
            autoplay: true,
            arrows: false,
            dots: false,
            pauseOnHover: false,
            pauseOnFocus: false,
            autoplaySpeed: 3000,
            responsive: [
                { breakpoint: 1199, settings: { slidesToShow: 3 } },
                { breakpoint: 992, settings: { slidesToShow: 2 } },
                { breakpoint: 451, settings: { slidesToShow: 1, variableWidth: false } }
            ]
        });
    });
    // counter section
    $(function () {
        const $counters = $(".counter-box h2");
        if (!$counters.length) return;
        let started = false;
        const animate = $el => {
            const txt = $el.text().trim(), k = /k/i.test(txt), plus = /\+/.test(txt),
                target = $el.data("target") || parseFloat(txt) * (k ? 1000 : 1);
            let val = 0, step = target / 125;
            (function run() {
                val += step;
                if (val < target) {
                    $el.text(Math.floor(val));
                    requestAnimationFrame(run);
                } else {
                    $el.text(k ? target / 1000 + "k" + (plus ? "+" : "") : target);
                }
            })();
        };
        new IntersectionObserver(entries => {
            if (entries[0].isIntersecting && !started) {
                $counters.each((_, el) => animate($(el)));
                started = true;
            }
        }, { threshold: 0.5 }).observe($(".counter-section")[0]);
    });
    // testimonial section
    $(function () {
        const $slider = $('.testimonial-autoplay').slick({
            slidesToShow: 1,
            slidesToScroll: 1,
            autoplay: true,
            autoplaySpeed: 3000,
            arrows: false,
            dots: false,
            infinite: true,
            pauseOnHover: false,
            pauseOnFocus: false
        });
        $(document)
            .on('click', '.testimonial-prev-arrow', () => $slider.slick('slickPrev'))
            .on('click', '.testimonial-next-arrow', () => $slider.slick('slickNext'));
    });
    // faq section
    $(function () {
        const $items = $(".faq-item");
        $items.each((i, item) => {
            const $arrow = $(item).find(".faq-arrow");
            if (i === 0) {
                $(item).addClass("active");
                $arrow.attr("src", "./assets/images/faq/green-arrow.svg");
            } else {
                $(item).removeClass("active");
                $arrow.attr("src", "./assets/images/faq/black-arrow.svg");
            }
        });
        $(document).on("click", ".faq-item", function () {
            $items.each((_, i) => {
                const $arr = $(i).find(".faq-arrow");
                $(i).removeClass("active");
                $arr.attr("src", "./assets/images/faq/black-arrow.svg");
            });
            $(this).addClass("active");
            $(this).find(".faq-arrow").attr("src", "./assets/images/faq/green-arrow.svg");
        });
    });
    // single blog video play
    $(function () {
        const $thumb = $(".video-thumbnail"),
            $btn = $(".single-blog-video-btn"),
            $video = $(".responsive-video");
        if (!$btn.length || !$video.length) return;
        $btn.on("click", () => {
            $thumb.add($btn).css("opacity", 0);
            setTimeout(() => {
                $thumb.add($btn).hide();
                $video.show().css("opacity", 1)[0].play();
            }, 300);
        });
        $video.on("ended", () => {
            $video.css("opacity", 0);
            setTimeout(() => {
                $video.hide();
                $thumb.add($btn).show();
                setTimeout(() => $thumb.add($btn).css("opacity", 1), 50);
                $video[0].currentTime = 0;
            }, 300);
        });
    });
    // team progress section
    $(function () {
        const $section = $(".progress-section");
        if (!$section.length) return;
        const animateProgress = () => {
            $(".progress-bar .progress-item").each(function () {
                const $item = $(this).find(".progress"),
                    target = $item.data("progress"),
                    $val = $(this).find(".item-value");
                let i = 0;
                const interval = setInterval(() => {
                    if (i <= target) {
                        $item.css("width", i + "%");
                        $val.text(i + "%");
                        i++;
                    } else clearInterval(interval);
                }, 30);
            });
        };
        new IntersectionObserver((entries, obs) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateProgress();
                    obs.unobserve(entry.target);
                }
            });
        }, { threshold: 0.3 }).observe($section[0]);
    });
    // gallery popup modal
    $(function () {
        const $gallery = $(".gallery-wrapper .gallery-img"),
            $icons = $(".gallery-plus-icon"),
            $popup = $("#galleryPopup"),
            $img = $("#popupImage"),
            $close = $(".close-popup"),
            $next = $(".next-btn"),
            $prev = $(".prev-btn");
        if (!$popup.length || !$close.length || !$next.length || !$prev.length) return;
        let current = 0;
        $icons.on("click", function () {
            current = $icons.index(this);
            $img.attr("src", $gallery.eq(current).attr("src"));
            $popup.css("display", "flex");
        });
        $next.on("click", () => {
            current = (current + 1) % $gallery.length;
            $img.attr("src", $gallery.eq(current).attr("src"));
        });
        $prev.on("click", () => {
            current = (current - 1 + $gallery.length) % $gallery.length;
            $img.attr("src", $gallery.eq(current).attr("src"));
        });
        $close.add($popup).on("click", e => {
            if ($(e.target).is($popup) || $(e.target).is($close)) $popup.hide();
        });
    });
    // coming soon countdown
    $(function () {
        const $days = $("#days"),
            $hours = $("#hours"),
            $minutes = $("#minutes"),
            $seconds = $("#seconds"),
            launch = new Date("2026-04-25T10:00:00").getTime();
        const updateCountdown = () => {
            const diff = launch - Date.now();
            if (diff <= 0) {
                $days.add($hours).add($minutes).add($seconds).text(0);
                return;
            }
            $days.text(Math.floor(diff / 86400000));
            $hours.text(Math.floor((diff % 86400000) / 3600000));
            $minutes.text(Math.floor((diff % 3600000) / 60000));
            $seconds.text(Math.floor((diff % 60000) / 1000));
        };
        setInterval(updateCountdown, 1000);
        updateCountdown();
    });
    // hero sliders
    $(function () {
        $('.hero-slider-wrapper').slick({
            slidesToShow: 1,
            slidesToScroll: 1,
            autoplay: true,
            autoplaySpeed: 3000,
            fade: true,
            speed: 2000,
            arrows: false,
            dots: false,
            infinite: true,
            pauseOnHover: false,
            pauseOnFocus: false
        });
        $('.hero-slider-wrapper2').slick({
            slidesToShow: 1,
            slidesToScroll: 1,
            autoplay: true,
            autoplaySpeed: 3000,
            fade: true,
            speed: 1000,
            arrows: false,
            dots: false,
            infinite: true,
            pauseOnHover: false,
            pauseOnFocus: false
        });
        $('.hero-slider-wrapper4').slick({
            slidesToShow: 1,
            slidesToScroll: 1,
            autoplay: true,
            autoplaySpeed: 6000,
            fade: true,
            speed: 2000,
            arrows: false,
            dots: false,
            infinite: true,
            pauseOnHover: false,
            pauseOnFocus: false
        });
    });
    // hero video popup
    $(function () {
        const $popup = $("#videoPopup"),
            video = $("#popupVideo")[0];
        $(document).on("click", ".video-ring", () => {
            $popup.addClass("active");
            video.currentTime = 0;
            video.play();
        });
        $(document).on("click", ".video-popup-close", e => {
            e.stopPropagation();
            $popup.removeClass("active");
            video.pause();
            video.currentTime = 0;
        });
        $popup.on("click", e => {
            if (e.target === e.currentTarget) {
                $popup.removeClass("active");
                video.pause();
                video.currentTime = 0;
            }
        });
    });
    // custom select dropdown
    $(function () {
        $(document).on("click", ".select-head", function () {
            const $select = $(this).closest(".custom-select");
            $(".custom-select").not($select).removeClass("open").find(".select-list").hide();
            $select.toggleClass("open").find(".select-list").toggle();
        });
        $(document).on("click", ".select-list li", function () {
            const $select = $(this).closest(".custom-select");
            $select.find(".selected-text").text($(this).text());
            $(this).addClass("active").siblings().removeClass("active");
            $select.removeClass("open").find(".select-list").hide();
        });
        $(document).on("click", function (e) {
            if (!$(e.target).closest(".custom-select").length) {
                $(".custom-select").removeClass("open").find(".select-list").hide();
            }
        });
    });
    // projects slider
    $(function () {
        $('.projects-slider').slick({
            slidesToShow: 5,
            slidesToScroll: 1,
            autoplay: true,
            autoplaySpeed: 3000,
            arrows: false,
            dots: false,
            infinite: true,
            pauseOnHover: false,
            pauseOnFocus: false,
            responsive: [
                { breakpoint: 1400, settings: { slidesToShow: 4 } },
                { breakpoint: 992, settings: { slidesToShow: 3 } },
                { breakpoint: 768, settings: { slidesToShow: 2 } },
                { breakpoint: 481, settings: { slidesToShow: 1 } }
            ]
        });
        $('.single-projects2-autoplay').slick({
            slidesToShow: 2,
            slidesToScroll: 1,
            autoplay: true,
            autoplaySpeed: 3000,
            arrows: false,
            dots: false,
            infinite: true,
            pauseOnHover: false,
            pauseOnFocus: false,
            responsive: [
                { breakpoint: 481, settings: { slidesToShow: 1 } }
            ]
        });
    });
})(jQuery);