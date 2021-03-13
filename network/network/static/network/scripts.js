document.addEventListener('DOMContentLoaded', function() {
    domain_name = window.location.pathname
    domain_url = window.location.href
    console.log("Loading domain", domain_name.substring(domain_name.lastIndexOf('/') + 1))
    if (domain_name == '/profile'){
        console.log("Loading profile page", domain_name)
    }

    // display_post(current_page)
    display_posts(domain_name)
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

function display_posts(page) {

    if (page.includes('/profile')) {
        console.log("Loading profile page: ", page)
        profile();
        return;
    }
    if (page == '/all') {
        all();
        return;
    }
    if (page == 'http://127.0.0.1:8000/following') {
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
    const container = document.createElement('div')
    container.setAttribute('id', 'post-container')
    document.querySelector('#all-post-container').append(container)
    if (post != undefined) {
        let numPosts = post.length;
        for (let counter = 0; counter < numPosts; counter++) {
            const div = document.createElement('div');
            div.setAttribute('class', 'post-item')

            let post_content = `${post[counter].user} ${post[counter].body} ${post[counter].timestamp}`
            div.innerHTML = post_content
            document.querySelector('#post-container').append(div)
        }
    } else {
        document.querySelector('#all-posts-container').innerHTML = 'No posts to display'
    }
    })
}


function all() {
    // Load only the posts made by the profile's user
    fetch('posts/all')
    .then(response => response.json())
    .then(post => {
    const container = document.createElement('div')
    container.setAttribute('id', 'post-container')
    document.querySelector('#all-post-container').append(container)
    if (post != undefined) {
        let numPosts = post.length;
        for (let counter = 0; counter < numPosts; counter++) {

            // Create a box to hold posts
            const div = document.createElement('div');
            div.setAttribute('class', 'post-item');

            const div_post = document.createElement('div');
            div_post.innerHTML = `${post[counter].body} ${post[counter].timestamp}`;
            
            // Create a link from a username to direct to user's profile
            const a = document.createElement('a');
            a.setAttribute('class', 'profile-link');
            a.href=`profile/${post[counter].user}`
            a.innerHTML = `${post[counter].user}`;

            // Add elements to container
            div.append(a)
            div.append(div_post);
            document.querySelector('#post-container').append(div)
        }
    } else {
        document.querySelector('#all-posts-container').innerHTML = 'No posts to display'
    }
    })
}

function display_post() {
    console.log("Displaying posts...")
    fetch('posts/all_posts')
    .then(response => response.json())
    .then(post => {
    const container = document.createElement('div')
    container.setAttribute('id', 'post-container')
    document.querySelector('#all-post-container').append(container)
    if (post != undefined) {
        let numPosts = post.length;
        for (let counter = 0; counter < numPosts; counter++) {
            const div = document.createElement('div');
            div.setAttribute('class', 'post-item')

            let post_content = `${post[counter].user} ${post[counter].body} ${post[counter].timestamp}`
            div.innerHTML = post_content
            document.querySelector('#post-container').append(div)
        }
    } else {
        document.querySelector('#all-posts-container').innerHTML = 'No posts to display'
    }
    })
}


function load_page(page) {
    document.querySelector('#profile-view').style.display = 'block';
    console.log("loading page from load_page()")
    // Load page depending on Page parameter
    if (page === 'profile') {
        profile();
        return;
    }

    if (page === 'following') {
        following();
        return;
    }

    if (page === 'all-posts') {
        all_posts();
        return;
    }
}


function following() {
    document.querySelector('#following-view').style.display = 'block';
    document.querySelector('#profile-view').style.display = 'none';
    document.querySelector('#all-posts-view').style.display = 'none';
}


function all_posts() {
    document.querySelector('#all-posts-view').style.display = 'block';
    document.querySelector('#profile-view').style.display = 'none';
    document.querySelector('#all-posts-view').style.display = 'none';

}