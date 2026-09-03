(function () {
  "use strict";

  function openPicker(event) {
    var button = event.target.closest("[data-picker-url]");
    if (!button) {
      return;
    }

    var fieldId = button.dataset.fieldId;
    var url = new URL(button.dataset.pickerUrl, window.location.origin);
    url.searchParams.set("field_id", fieldId);
    window.open(
      url.toString(),
      "media_asset_picker",
      "width=1100,height=760,resizable=yes,scrollbars=yes"
    );
  }

  function receiveSelection(event) {
    if (event.origin !== window.location.origin || !event.data) {
      return;
    }
    if (event.data.type !== "media-asset-selected") {
      return;
    }

    var field = document.getElementById(event.data.fieldId);
    if (!field) {
      return;
    }
    field.value = event.data.value;
    field.dispatchEvent(new Event("change", { bubbles: true }));
  }

  document.addEventListener("click", openPicker);
  window.addEventListener("message", receiveSelection);
})();
