/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ "./src/js/houses/house_list_filters.js":
/*!*********************************************!*\
  !*** ./src/js/houses/house_list_filters.js ***!
  \*********************************************/
/***/ (() => {

eval("document.addEventListener('DOMContentLoaded', function () {\n  var districtSelect = document.getElementById('district-select');\n  var municipalitySelect = document.getElementById('municipality-select');\n  var parishSelect = document.getElementById('parish-select');\n  var localeSelect = document.getElementById('locale-select');\n  if (!districtSelect.value) {\n    municipalitySelect.setAttribute('disabled', 'disabled');\n    parishSelect.setAttribute('disabled', 'disabled');\n    localeSelect.setAttribute('disabled', 'disabled');\n  }\n  districtSelect.addEventListener('change', function () {\n    var selectedDistrict = this.value;\n    Array.from(municipalitySelect.options).forEach(function (option) {\n      option.style.display = option.getAttribute('data-district') === selectedDistrict ? 'block' : 'none';\n    });\n    municipalitySelect.removeAttribute('disabled');\n    municipalitySelect.value = '';\n  });\n  municipalitySelect.addEventListener('change', function () {\n    var selectedMunicipality = this.value;\n    Array.from(parishSelect.options).forEach(function (option) {\n      option.style.display = option.getAttribute('data-municipality') === selectedMunicipality ? 'block' : 'none';\n    });\n    parishSelect.removeAttribute('disabled');\n    parishSelect.value = '';\n  });\n  parishSelect.addEventListener('change', function () {\n    var selectedParish = this.value;\n    Array.from(localeSelect.options).forEach(function (option) {\n      option.style.display = option.getAttribute('data-parish') === selectedParish ? 'block' : 'none';\n    });\n    localeSelect.removeAttribute('disabled');\n    localeSelect.value = '';\n  });\n  document.getElementById('reset-filters').addEventListener('click', function () {\n    window.location.href = window.location.pathname;\n  });\n});\n\n//# sourceURL=webpack://frontend/./src/js/houses/house_list_filters.js?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = {};
/******/ 	__webpack_modules__["./src/js/houses/house_list_filters.js"]();
/******/ 	
/******/ })()
;