<p align="center">
</p>
<p align="center">
    <h1 align="center">USED-CAR-PRICE-DATA-ANALYSIS</h1>
</p>
<p align="center">
   This project aims to analyze data related to used car prices to derive insights that can aid in understanding the factors influencing car prices in the secondary market.
</p>

<h2><img src="https://cdn-icons-png.flaticon.com/128/6293/6293965.png" width="20"> Overview </h2>

This is final project for the **[DataTalks Data Engineering zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp)**. 
In which I have made a end-to-end pipeline 
- Extracting data from the source and loading it into a Google Storage Bucket. 
- Creating Big Query Table from the storage data.
- Visualize using the looker studio 
<hr>

<h2><img src="https://cdn-icons-png.flaticon.com/128/1694/1694262.png" width="20"> Motivation </h2>
<p> The motivation for this project is to find trend of the second hand car market in the US. The second-hand car market offers affordability, sustainability, and community engagement, providing access to quality vehicles at lower prices while reducing waste and promoting resourcefulness in transportation choices.

This analyis will help the people to find solutions for 
<ul>
<li>what cars sells the most in the second hand market ?</li> 
<li>In which states does the second hand car market is booming ?</li>
<li>In which state can we open does the second hand car market busniess ?</li>
</ul>
These are some of the examples this analysis will answer.
</p>

---
<h2> <img src="https://cdn-icons-png.flaticon.com/128/1664/1664210.png" width="20"> Architectural diagram </h2>
<img src="https://github.com/Hari-cbe/Random-resourses/blob/main/Used-car-price-data/images/Untitled%20Diagram.drawio.png?raw=true>"

---

##  Repository Structure

```sh
└── Used-Car-Price-data-analysiss/
    ├── Dockerfile
    ├── README.md
    ├── dags
    │   ├── __pycache__
    │   └── sourcetobucket.py
    ├── dbt-env
    │   ├── bin
    │   ├── lib
    │   ├── lib64
    │   ├── pyvenv.cfg
    │   └── share
    ├── docker-compose.yaml
    ├── logs
    │   ├── dag_id=check_errors
    │   ├── dag_id=source_to_gcs
    │   ├── dag_id=test_airflow
    │   ├── dag_processor_manager
    │   ├── dbt.log
    │   └── scheduler
    ├── requirements.txt
    ├── terraform
    │   ├── .terraform
    │   ├── .terraform.lock.hcl
    │   ├── main.tf
    │   ├── terraform.tfstate
    │   ├── terraform.tfstate.backup
    │   └── variables.tf
    └── used_car_price_analysis
        ├── .gitignore
        ├── analyses
        ├── dbt_project.yml
        ├── macros
        ├── models
        ├── package-lock.yml
        ├── packages.yml
        ├── seeds
        ├── snapshots
        └── tests
```

---

##  Getting Started

**Technologies used**

* **Python**: `version x.y.z`

###  Installation

<h4>From <code>source</code></h4>

> 1. Clone the Used-Car-Price-data-analysiss repository:
>
> ```console
> $ git clone https://github.com/Hari-cbe/Used-Car-Price-data-analysiss.git
> ```
>
> 2. Change to the project directory:
> ```console
> $ cd Used-Car-Price-data-analysiss
> ```
>
> 3. Install the dependencies:
> ```console
> $ pip install -r requirements.txt
> ```

###  Usage

<h4>From <code>source</code></h4>

> Run Used-Car-Price-data-analysiss using the command below:
> ```console
> $ python main.py
> ```

###  Tests

> Run the test suite using the command below:
> ```console
> $ pytest
> ```

---

##  Project Roadmap

- [X] `► INSERT-TASK-1`
- [ ] `► INSERT-TASK-2`
- [ ] `► ...`

---

##  Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Report Issues](https://github.com/Hari-cbe/Used-Car-Price-data-analysiss.git/issues)**: Submit bugs found or log feature requests for the `Used-Car-Price-data-analysiss` project.
- **[Submit Pull Requests](https://github.com/Hari-cbe/Used-Car-Price-data-analysiss.git/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Join the Discussions](https://github.com/Hari-cbe/Used-Car-Price-data-analysiss.git/discussions)**: Share your insights, provide feedback, or ask questions.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone https://github.com/Hari-cbe/Used-Car-Price-data-analysiss.git
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to github**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
</details>

<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="center">
   <a href="https://github.com{/Hari-cbe/Used-Car-Price-data-analysiss.git/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=Hari-cbe/Used-Car-Price-data-analysiss.git">
   </a>
</p>
</details>

---

##  License

This project is protected under the [SELECT-A-LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

---

##  Acknowledgments

- List any resources, contributors, inspiration, etc. here.

[**Return**](#-overview)

---