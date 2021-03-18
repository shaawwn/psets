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

// function follow() {
//     // Follow a user with the click of a button!
//     console.log("Follow button pressed!")
//     profile_id = window.location.pathname.substring(window.location.pathname.lastIndexOf('/') + 1)

//     fetch(`/follow`)
//     .then(response => response.json())
//     .then(profile => {
//         console.log("Inside fetch, profile: ", profile)
//         if (profile.following === profile_id) {
//             fetch('/follow', {
//                 method: 'POST',
//                 following: false
//             })
//         } else {
//             console.log("Inside else", profile)
//             fetch('/follow', {
//                 method: 'POST', 
//                 following: profile_id,
//                 }
//         )
//     }
//     console.log("Enf of loop", profile)
//     })

// }


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

// function display_post() {
    // I think this is obsolete, but don't delete yet
//     console.log("Displaying posts...")
//     fetch('posts/all_posts')
//     .then(response => response.json())
//     .then(post => {
//         display_box(post);
//     })
// }



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

            document.querySelector('#post-container').append(div)
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


function edit_post() {
    // When users click the edit button, load a textarea populated with the current content and allow users to edit content
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