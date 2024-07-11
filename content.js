document.addEventListener('mouseover', function (event) {
  let tagName = event.target.tagName.toLowerCase();
  let className = event.target.className;
  let id = event.target.id;
  console.log(`${tagName}, ${className}, ${id}`);
  // console.log(event.target);
  if (tagName === 'ytd-video-preview') {
    let videoThumbnail = event.target;
    // showPopup(videoThumbnail);
  } else if (tagName === 'div' && className === 'style-scope ytd-video-preview') {
    console.log('onhover');
    let videoThumbnail = document.querySelector('#media-container-link');
    console.log(videoThumbnail);
    showPopup(videoThumbnail);
    // console.log(event.target);
    // console.log(event.parentElement);
    // let videoThumbnail = event.target.parentElement;
    // showPopup(videoThumbnail);
  }
});

function showPopup(thumbnail) {
  let popup = document.createElement('div');
  popup.id = 'video-info-popup';
  popup.innerHTML = `
    <div id="loading">Loading...</div>
    <div id="clickbait-rating"></div>
    <div id="video-summary"></div>
    <div id="comments-summary"></div>
  `;
  document.body.appendChild(popup);

  let rect = thumbnail.getBoundingClientRect();
  popup.style.top = `${rect.top + window.scrollY + rect.height}px`;
  popup.style.left = `${rect.left + window.scrollX}px`;

  fetchVideoInfo(thumbnail);
}

function fetchVideoInfo(thumbnail) {
  // let videoId = thumbnail.querySelector('#video-preview-container').querySelector('#media-container').querySelector('a').href.split('v=')[1];
  let videoId = thumbnail.href.split('v=')[1];
  
  fetch(`https://507e6687-4236-4ae1-9220-c40483674512-00-9piah707l5p1.spock.replit.dev/video-info?videoId=${videoId}`)
    .then(response => response.json())
    .then(data => {
      document.getElementById('loading').style.display = 'none';
      document.getElementById('clickbait-rating').innerText = `🥇 Clickbait Rating: ${data.clickbaitRating}`;
      document.getElementById('video-summary').innerText = `🥈 Video Summary: ${data.videoSummary}`;
      document.getElementById('comments-summary').innerText = `🥉 TL;DR of Comments: ${data.commentsSummary}`;
    })
    .catch(error => {
      console.error('Error fetching video info:', error);
    });
}

