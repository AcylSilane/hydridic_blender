<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
<img alt="Python" src="https://img.shields.io/badge/python-%2314354C.svg?style=appveyor&logo=python&logoColor=white"/>  <img alt="Blender" src="https://img.shields.io/badge/blender-%23F5792A.svg?style=appveyor&logo=blender&logoColor=white"/>

[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

[![Stargazers][stars-shield]][stars-url]
[![Forks][forks-shield]][forks-url]
[![Contributors][contributors-shield]][contributors-url]
[![Issues][issues-shield]][issues-url]

![Master Tests](https://github.com/AcylSilane/hydridic_blender/actions/workflows/test_lint_master.yml/badge.svg?branch=master)
![Dev Tests](https://github.com/AcylSilane/hydridic_blender/actions/workflows/test_lint_dev.yml/badge.svg?branch=dev)





<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/AcylSilane/hydridic_blender">
    <img src="assets/logo.png" alt="Logo" width="256" height="256">
  </a>
</p>

<h3 align="center">Hydridic Blender</h3>

<p align="center">
    This addon helps import chemical species to blender. 
    <br />
    <a href="https://github.com/AcylSilane/hydridic_blender"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <!-- <a href="https://github.com/AcylSilane/hydridic_blender">View Demo</a>
    · -->
    <a href="https://github.com/AcylSilane/hydridic_blender/issues">Report Bug</a>
    ·
    <a href="https://github.com/AcylSilane/hydridic_blender/issues">Request Feature</a>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <!-- <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li> -->
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->

## About The Project

Hydridic Blender is a Blender addon that's designed to make it easier to create illustrations of molecules and crystals.
It was inspired by the
wonderful [Atomic Blender](https://docs.blender.org/manual/en/latest/addons/import_export/mesh_atomic.html) addon that
comes stock with most Blender installations. Hydridic Blender tries to build on this idea, to give users a higher level
of control over their 3D models.

The logo here are the letters "H" and "B", dressed up to resemble the half up/down
arrows [commonly used to represent electrons in orbital diagrams](https://chem.libretexts.org/Courses/Mount_Royal_University/Chem_1201/Unit_2._Periodic_Properties_of_the_Elements/2.02%3A_Electron_Configurations)
, superimposed on an orange (for Blender :D ) [Frost Circle](https://en.wikipedia.org/wiki/Hückel_method).

### Built With

* [The Atomic Simulation Environment](https://wiki.fysik.dtu.dk/ase/)
* [Blender's Python API](https://docs.blender.org/api/current/index.html#)

<!-- GETTING STARTED -->
<!-- ## Getting Started

To get started with Hydridic Blender, follow the guide below.

### Prerequisites

TODO: Add pre-requisites section

### Installation

TODO: Add installation instructions -->



<!-- USAGE EXAMPLES -->

## Usage

Currently, the addon supports the import of any chemical format supported by the Atomic Simulation Environment (XYZ,
VASP, PDB, etc.) of both periodic and non-periodic varieties. Bonds are not currently calculated drawn, but this is
something currently being worked on.



<!-- ROADMAP -->

## Roadmap

See the [open issues](https://github.com/AcylSilane/hydridic_blender/issues) for a list of proposed features (and known
issues).



<!-- CONTRIBUTING -->

## Contributing

This is currently a 1-person project, being done in the author's spare time. That being said, any contributions are
welcome! If you'd like to help out, please do the following:

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
6. Keep on Being Awesome!

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->

## Contact

James Dean - message me via GitHub

Project Link: [https://github.com/AcylSilane/hydridic_blender](https://github.com/AcylSilane/hydridic_blender)



<!-- ACKNOWLEDGEMENTS -->

## Acknowledgements

* [The Best README Template](https://github.com/othneildrew/Best-README-Template)
* The [Blender Development](https://marketplace.visualstudio.com/items?itemName=JacquesLucke.blender-development) VSCode
  extension by Jacques Lucke
*
This [excellent blog post](https://b3d.interplanety.org/en/using-microsoft-visual-studio-code-as-external-ide-for-writing-blender-scripts-add-ons/)
by Nikita, which greatly helped in getting autocomplete/linting working for Blender's Python API

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/AcylSilane/hydridic_blender.svg?style=appveyor

[contributors-url]: https://github.com/AcylSilane/hydridic_blender/graphs/contributors

[forks-shield]: https://img.shields.io/github/forks/AcylSilane/hydridic_blender.svg?style=appveyor

[forks-url]: https://github.com/AcylSilane/hydridic_blender/network/members

[stars-shield]: https://img.shields.io/github/stars/AcylSilane/hydridic_blender.svg?style=appveyor

[stars-url]: https://github.com/AcylSilane/hydridic_blender/stargazers

[issues-shield]: https://img.shields.io/github/issues/AcylSilane/hydridic_blender.svg?style=appveyor

[issues-url]: https://github.com/AcylSilane/hydridic_blender/issues

[license-shield]: https://img.shields.io/github/license/AcylSilane/hydridic_blender.svg?style=appveyor

[license-url]: https://github.com/AcylSilane/hydridic_blender/blob/master/LICENSE.txt

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=appveyor&logo=linkedin&colorB=555

[linkedin-url]: https://linkedin.com/in/DeanJamesR
