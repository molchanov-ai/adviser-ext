// 1.5 sec delay for deliberate user's video choice
let timerId = null;

let url = 'https://507e6687-4236-4ae1-9220-c40483674512-00-9piah707l5p1.spock.replit.dev';

document.addEventListener('mouseover', function (event) {
  let tagName = event.target.tagName.toLowerCase();
  let className = event.target.className;
  let id = event.target.id;
  console.log(`${tagName}, ${className}, ${id}`);

  let staticPreviewClassName = 'yt-core-image yt-core-image--fill-parent-height yt-core-image--fill-parent-width yt-core-image--content-mode-scale-aspect-fill yt-core-image--loaded';
  let dynamicPreviewCondition = tagName === 'div' && className === 'style-scope ytd-video-preview';

  // Mouse at popup
  if (className != staticPreviewClassName && (className == 'video-info-popup' || tagName == 'svg' ||
    tagName == 'path' || tagName == 'img' ||
    className == 'style-scope tp-yt-app-drawer' ||
    className == 'yt-simple-endpoint style-scope ytd-mini-guide-entry-renderer' ||
    className == '' || tagName == 'rect' || className == 'ldBar')) {
    return;
  }
  // mouse at thumbnail
  if (className == staticPreviewClassName || dynamicPreviewCondition) {
    let popup = document.querySelector('.video-info-popup');

    if (className == staticPreviewClassName) {
      var videoThumbnail = event.target.parentNode.parentNode;
    } else {
      var videoThumbnail = document.querySelector('#media-container-link');
    }

    if (videoThumbnail.href.includes('v=')) {
      var videoId = videoThumbnail.href.split('v=')[1].split('&')[0];
    } else if (videoThumbnail.href.includes('shorts')) {
      var videoId = videoThumbnail.href.split('/').at(-1);
    } else {
      console.error('Incompatible state');
      return;
    }

    if (videoId.includes('&')) {
      videoId = videoId.split('&')[0];
    }

    if (popup != null && popup.id.includes(videoId)) {
      return;
    }

    let popups = document.querySelectorAll('.video-info-popup');
    popups.forEach((e) => e.remove());

    if (timerId != null) {
      clearTimeout(timerId);
      timerId = null;
    }

    timerId = setTimeout(() => showPopup(videoThumbnail, videoId), 1500);
  } else { // Mouse not on thumbnail and popup
    if (timerId != null) {
      clearTimeout(timerId);
      timerId = null;
    }

    let popups = document.querySelectorAll('.video-info-popup');
    popups.forEach((e) => e.remove());
  }
});

function showPopup(thumbnail, videoId) {
  let popup = document.createElement('div');
  let popupId = `video-info-popup-${videoId}`;

  popup.id = popupId;
  popup.className = 'video-info-popup';
  popup.style.maxWidth = '600px';
  popup.innerHTML = `
    <div id="loading"></div>
    <div id="clickbait-rating"></div>
    <div id="video-summary"></div>
    <div id="comments-summary"></div>
    <div id="justification"></div>
  `;
  document.body.appendChild(popup);

  var bar1 = new ldBar(popup.querySelector('#loading'), {
    "preset": "rainbow",
    "stroke-width": 10,
    "stroke": "data:ldbar/res,gradient(0,1,#9df,#9fd,#df9,#fd9)",
    "path": "M10 20Q20 5 30 20Q40 35 50 20Q60 5 70 20Q80 35 90 20"
  });
  bar1.set(100);

  let rect = thumbnail.getBoundingClientRect();
  popup.style.top = `${rect.top + window.scrollY + rect.height}px`;
  popup.style.left = `${rect.left + window.scrollX}px`;

  fetchVideoInfo(videoId, popupId);
}

function fetchVideoInfo(videoId, popupId) {
  let parent = document.getElementById(popupId);
  fetch(`${url}/video-info?videoId=${videoId}`)
    .then(response => response.json())
    .then(data => {
      parent.querySelector('#loading').remove();
      parent.querySelector('#clickbait-rating').innerHTML = `🥇 <b>Clickbait Rating:</b> ${data.clickbaitRating}`;
      parent.querySelector('#video-summary').innerHTML = `🥈 <b>Video Summary:</b> ${data.videoSummary}`;
      parent.querySelector('#comments-summary').innerHTML = `🥉 <b>TL;DR of Comments:</b> ${data.commentsSummary}`;
      parent.querySelector('#justification').innerHTML = `❗️ <b>Justification:</b> ${data.justification}`;
    })
    .catch(error => {
      parent.querySelector('#loading').remove();
      parent.querySelector('#clickbait-rating').innerHTML = `<b>Error:</b> sorry, please try again. Also note that we don't support broadcasts at the moment`;
      console.error('Error fetching video info:', error);
    });
}