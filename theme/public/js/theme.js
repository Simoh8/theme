frappe.ready(function() {
    new WOW().init();
    
    $('a[href*="#"]').on('click', function(e) {
        e.preventDefault();
        
        $('html, body').animate(
            {
                scrollTop: $($(this).attr('href')).offset().top - 80,
            },
            500,
            'linear'
        );
    });
    
    $('.newsletter-form').submit(function(e) {
        e.preventDefault();
        var email = $(this).find('input[type="email"]').val();
        
        frappe.call({
            method: "theme.api.subscribe_newsletter",
            args: {
                email: email
            },
            callback: function(r) {
                if (r.message === "success") {
                    frappe.msgprint(__("Thank you for subscribing!"));
                    $('.newsletter-form')[0].reset();
                }
            }
        });
    });
    
    $('#contact-form').submit(function(e) {
        e.preventDefault();
        frappe.call({
            method: "theme.theme.api.submit_contact_form",
            args: {
                name: $(this).find("input[name='name']").val(),
                email: $(this).find("input[name='email']").val(),
                subject: $(this).find("input[name='subject']").val(),
                message: $(this).find("textarea[name='message']").val()
            },
            callback: function(r) {
                if (r.message === "success") {
                    frappe.msgprint(__("Thank you for your message! We'll get back to you soon."));
                    $("#contact-form")[0].reset();
                }
            }
        });
    });
    
    $(window).scroll(function() {
        if ($(this).scrollTop() > 50) {
            $('.navbar').addClass('navbar-scrolled');
        } else {
            $('.navbar').removeClass('navbar-scrolled');
        }
    });
});

$('#demo-request-form').submit(function(e) {
    e.preventDefault();
    var btn = $(this).find('[type="submit"]');
    var btn_text = btn.html();
    
    btn.prop('disabled', true).html('<span class="spinner-border spinner-border-sm mr-2" role="status" aria-hidden="true"></span>Processing...');
    
    var form_data = {
        full_name: $('#full-name').val(),
        company: $('#company').val(),
        email: $('#email').val(),
        phone: $('#phone').val(),
        job_title: $('#job-title').val(),
        industry: $('#industry').val(),
        solutions: $('input[name="solutions"]:checked').map(function() {
            return this.value;
        }).get().join(', '),
        message: $('#message').val(),
        subscribe: $('#subscribe').is(':checked') ? 'Yes' : 'No'
    };
    
    frappe.call({
        method: "theme.api.submit_demo_request",
        args: {
            data: form_data
        },
        callback: function(r) {
            if (r.message === "success") {
                // Show success message
                frappe.msgprint({
                    title: __('Thank You!'),
                    indicator: 'green',
                    message: __('Your demo request has been submitted successfully. Our team will contact you shortly to schedule your demo.')
                });
                
                // Reset form
                $('#demo-request-form')[0].reset();
            } else {
                frappe.msgprint({
                    title: __('Error'),
                    indicator: 'red',
                    message: __('There was an error submitting your request. Please try again or contact us directly.')
                });
            }
            
            // Reset button
            btn.prop('disabled', false).html(btn_text);
        },
        error: function() {
            frappe.msgprint({
                title: __('Error'),
                indicator: 'red',
                message: __('There was an error submitting your request. Please try again or contact us directly.')
            });
            
            // Reset button
            btn.prop('disabled', false).html(btn_text);
        }
    });
});


// Pricing Toggle
$('input[name="pricing-option"]').change(function() {
    if ($(this).attr('id') === 'monthly') {
        $('.price').removeClass('d-none');
        $('.price-annual').addClass('d-none');
    } else {
        $('.price').addClass('d-none');
        $('.price-annual').removeClass('d-none');
    }
});

// Contact Form Submission
$('#contact-form').submit(function(e) {
    e.preventDefault();
    var btn = $(this).find('[type="submit"]');
    var btn_text = btn.html();
    
    btn.prop('disabled', true).html('<span class="spinner-border spinner-border-sm mr-2" role="status" aria-hidden="true"></span>Sending...');
    
    frappe.call({
        method: "theme.theme.api.submit_contact_form",
        args: {
            name: $('#name').val(),
            email: $('#email').val(),
            subject: $('#subject').val(),
            message: $('#message').val(),
            subscribe: $('#subscribe').is(':checked') ? 'Yes' : 'No'
        },
        callback: function(r) {
            if (r.message === "success") {
                frappe.msgprint({
                    title: __('Thank You!'),
                    indicator: 'green',
                    message: __('Your message has been sent successfully. We will get back to you soon.')
                });
                $('#contact-form')[0].reset();
            } else {
                frappe.msgprint({
                    title: __('Error'),
                    indicator: 'red',
                    message: __('There was an error sending your message. Please try again later.')
                });
            }
            btn.prop('disabled', false).html(btn_text);
        }
    });
});

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
});

$('a[href^="#"]').on('click', function(e) {
    e.preventDefault();
    
    $('html, body').animate(
        {
            scrollTop: $($(this).attr('href')).offset().top - 80,
        },
        500,
        'linear'
    );
});

new WOW().init();

$('.solution-form').submit(function(e) {
    e.preventDefault();
    var form = $(this);
    var formData = form.serialize();
    var submitBtn = form.find('[type="submit"]');
    var btnText = submitBtn.html();
    
    submitBtn.prop('disabled', true).html('<span class="spinner-border spinner-border-sm mr-2" role="status" aria-hidden="true"></span>Processing...');
    
    frappe.call({
        method: "theme.api.submit_solution_interest",
        args: {
            data: formData,
            solution: form.data('solution')
        },
        callback: function(r) {
            if (r.message === "success") {
                frappe.msgprint({
                    title: __('Thank You!'),
                    indicator: 'green',
                    message: __('Your request has been submitted. Our team will contact you shortly.')
                });
                form[0].reset();
            } else {
                frappe.msgprint({
                    title: __('Error'),
                    indicator: 'red',
                    message: __('There was an error submitting your request. Please try again later.')
                });
            }
            submitBtn.prop('disabled', false).html(btnText);
        }
    });
});
