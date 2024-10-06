/**
 * alerts using simply-notify
 */

function pushNotify(message, displayMsg) {
  new Notify({
    status: message,
    text: displayMsg,
    effect: "fade",
    speed: 300,
    customClass: null,
    customIcon: null,
    showIcon: true,
    showCloseButton: true,
    autoclose: true,
    autotimeout: 3000,
    type: "filled",
    position: "x-center",
    notificationsPadding: -10,
  });
}
