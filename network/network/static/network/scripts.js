document.addEventListener('DOMContentLoaded', function() {
    domain_name = window.location.pathname
    domain_url = window.location.href
    console.log("Loading domain", domain_name.substring(domain_name.lastIndexOf('/') + 1))
    if (domain_name == '/profile'){
        console.log("Loading profile page", domain_name)
    }

    // display_post(current_page)
    display_posts(domain_name)
    edit_post()
    document.querySelector('#post-submit').addEventListener('click', () => post());

    // Load All Posts
    // load_page('all-posts')
});


function post() {
    console.log("Before query")
    // Clear out composition fields


    document.querySelector("#post-form").onsubmit = function() {
        fetch('/posts', {
            method: 'POST',
            body: JSON.stringify({
                body: document.querySelector("#id_body").value
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result)
        })
        document.querySelector('#form-control body').value = '';
        return false;
    }
}


function follow() {
    profile_id = window.location.pathname.substring(window.location.pathname.lastIndexOf('/') + 1)

    fetch(`/follow/${profile_id}`)
    .then(response => response.json())
    .then(profile => {
        return;
    })
}


function display_posts(page) {

    if (page.includes('/profile')) {
        profile();
        return;
    }
    if (page == '/all') {
        all();
        return;
    }
    if (page == '/following') {
        following();
        return;
    }
} 


function profile() {
    // Load only the posts made by the profile's user
    profile_id = window.location.pathname.substring(window.location.pathname.lastIndexOf('/') + 1)
    console.log(`Loading profile...${profile_id}`)
    fetch(`posts/${profile_id}`)
    .then(response => response.json())
    .then(post => {

        // Get user id (Can move code from function directly here if bugs happen)
        const user_id = get_user(post)
        console.log(user_id)
        display_box(post, user_id)
    })
    if (document.querySelector('follow-button')) {
        document.querySelector('follow-button').onclick = follow
    }
}


function all() {
    // Load only the posts made by the profile's user Load all posts?
    fetch('posts/all')
    .then(response => response.json())
    .then(post => {
        const user_id = get_user(post)
        display_box(post, user_id);
})
}

function following() {
    // Load only posts from users that a user is folowing
    fetch('posts/following')
    .then(response => response.json())
    .then(post => {
        const user_id = get_user(post)
        display_box(post, user_id)
    })
}


function display_box(post, username) {
    // Manages the creation of user post containers, and fills containers using data from post request
    console.log("Displaybox username: ", username)
    const container = document.createElement('div')
    container.setAttribute('id', 'post-container')
    document.querySelector('#all-post-container').append(container)

    if (post != undefined) {
        let numPosts = post.length;
        for (let counter = 0; counter < numPosts; counter++) {
            const div = document.createElement('div');
            div.setAttribute('class', 'post-item')
            
            // Container for post body
            const div_post = document.createElement('div');
            div_post.setAttribute('class', 'post-body')
            div_post.innerHTML = `${post[counter].body} ${post[counter].timestamp}`

            // Link for poster's profile
            const a = document.createElement('a');
            a.setAttribute('class', 'profile-link');
            a.href=`profile/${post[counter].user}`;
            a.innerHTML = `${post[counter].user}`;

            // If a post is by current user, add edit button
            if (username == `${post[counter].user}`) {
                const button = document.createElement('button')
                button.setAttribute('class', 'edit-button')
                button.setAttribute('value', 'edit');
            }

            // Add post elements to post container
            div.append(a);
            div.append(div_post)

            // If a post is by current user, add edit button
            if (username == `${post[counter].user}`) {
                const button = document.createElement('button')
                button.setAttribute('class', 'edit-button')
                button.setAttribute('value', 'Edit')
                button.innerHTML = 'Edit'
                div.append(button)
            }

            document.querySelector('#all-post-container').append(div) // Changed from JUST 'post-container'
        }
    } else {
        document.querySelector('#all-posts-container').innerHTML = 'No posts to display'
    }
    return container;
}


function get_user(post) {
    const user_id = JSON.parse(document.getElementById('user_id').textContent);
    return user_id
}


function edit_post(id) {
    // Change post-body to a text area to edit post

    // const form = document.createElement('form')
    const edit_text = document.createElement('textarea');
    edit_text.setAttribute('class', 'text-edit')
    var post_id = "post " + id;
    var text = document.getElementById(post_id).innerText;
    console.log("Text inner text: ", text)
    edit_text.value = text
    console.log("Textbox content", text)
    // form.append(edit_text)
    
    var body_id = "post-body " + id;
    post_body = document.getElementById(body_id);
    to_replace = document.getElementById(post_id);
    post_body.replaceChild(edit_text, to_replace)

    // CSRF TOKENS
    let csrftoken = getCookie('csrftoken');
    
    document.getElementById(id).addEventListener('click', () => {
        console.log("TEXT AREA VALUE", edit_text.value)
        const post_id = parseInt(id);
        fetch(`posts/post/${post_id}`, {
            method: 'PUT', 
            headers: { "X-CSRFToken": csrftoken},
            body: JSON.stringify({
                body: edit_text.value
            }),

        })
        text = edit_text.value
        console.log(text, edit_text.value)

        to_replace = document.createElement('div')
        to_replace.setAttribute("id", "post_id")
        to_replace.setAttribute('class', 'post-body')
        to_replace.innerHTML = edit_text.value
        post_body.replaceChild(to_replace, edit_text)
    })
    return false;
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        console.log("IF STATEMENT FIRED")
        var cookies = document.cookie.split(';');
        console.log("COOKIES ARE: ", cookies)
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                console.log("COOKIE AFTER DECODING: ", cookieValue)
                break;
            }
        console.log("COOKIE IN FOR LOOP", cookie)
        }
    }

    return cookieValue;
}


function edit_text() {
    document.querySelector('.post-body').style.display = 'none';
    const text_edit = document.createElement('textarea')
    text_edit.innerHTML = document.querySelector('post-body').innerHTML
}




function all_posts() {
    document.querySelector('#all-posts-view').style.display = 'block';
    document.querySelector('#profile-view').style.display = 'none';
    document.querySelector('#all-posts-view').style.display = 'none';

}