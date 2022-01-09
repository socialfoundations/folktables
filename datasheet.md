Datasheet
=========

This datasheet covers both the prediction tasks we introduce and the
underlying US Census data sources. However, due to the extensive
documentation available about the US Census data we often point to
relevant available resources rather than recreating them here. 

Motivation
----------

-   **For what purpose was the dataset created?** Was there a specific
    task in mind? Was there a specific gap that needed to be filled?
    Please provide a description.

    The motivation for creating prediction tasks on top of US Census
    data was to extend the dataset ecosystem available for algorithmic
    fairness research as outlined in this paper.

-   **Who created the dataset (e.g., which team, research group) and on
    behalf of which entity (e.g., company, institution, organization)?**

    The new prediction tasks were created from available US Census data
    sources by Frances Ding, Moritz Hardt, John Miller, and Ludwig
    Schmidt.

-   **Who funded the creation of the dataset?** If there is an
    associated grant, please provide the name of the grantor and the
    grant name and number.

    Frances Ding, Moritz Hardt, and John Miller were employed by the
    University of California for the duration of this research project,
    funded by grants administered through the University of California.
    Ludwig Schmidt was employed by Toyota Research throughout this
    research project.

-   **Any other comments?**

    No.

Composition
-----------

-   **What do the instances that comprise the dataset represent (e.g.,
    documents, photos, people, countries)?** Are there multiple types of
    instances (e.g., movies, users, and ratings; people and interactions
    between them; nodes and edges)? Please provide a description.

    Each instance in our IPUMS Adult reconstruction represents an
    individual. Similarly, our datasets derived from ACS contains
    instances representing individuals. The ACS data our datasets are
    derived from also contain household-level information and the
    relationship between households and individuals.

-   **How many instances are there in total (of each type, if
    appropriate)?**

    Our IPUMS Adult reconstruction contains 49,531 rows, each with 14
    attributes.  The following table described the sizes of our datasets derived
    from ACS.
 
    |Task | Features | Datapoints |
    |-----|----------|------------|
    | ACSIncome         | 10       | 1,664,500  |
    | ACSPublicCoverage | 19       | 1,138,289  |
    | ACSMobility       | 21       | 620,937    |
    | ACSEmployment     | 17       | 3,236,107  |
    | ACSTravelTime     | 16       | 1,466,648  |

-   **Does the dataset contain all possible instances or is it a sample
    (not necessarily random) of instances from a larger set?** If the
    dataset is a sample, then what is the larger set? Is the sample
    representative of the larger set (e.g., geographic coverage)? If so,
    please describe how this representativeness was validated/verified.
    If it is not representative of the larger set, please describe why
    not (e.g., to cover a more diverse range of instances, because
    instances were withheld or unavailable)

    Both IPUMS Adult and our ACS datasets are samples of the US population.
    Please see Sections 2 and 3, and Appendices A and B of the [associated
    paper]() and the corresponding documentation provided by the
    US Census Bureau for complete details regarding the sampling distribution.
    Note that the per-instance weights have to be taken into account if the
    sample is meant to represent the US population.

-   **What data does each instance consist of?** "Raw" data (e.g.,
    unprocessed text or images) or features? In either case, please
    provide a description.

    Each instance consists of features. IPUMS Adult uses the same
    features as the original UCI Adult dataset. Appendix B of the [associated
    paper](https://arxiv.org/abs/2108.04884) and the corresponding documentation
    provided by the US Census Bureau describes each feature in our new datasets
    derived from ACS.

-   **Is there a label or target associated with each instance?** If so,
    please provide a description.

    Similar to UCI Adult, our IPUMS Adult reconstruction uses the income
    as label (where the continuous values as opposed to only the
    binarized values are now available). Appendix B in the [associated
    paper](https://arxiv.org/abs/2108.04884) describes the labels in our new
    datasets derived from ACS.

-   **Is any information missing from individual instances?** If so,
    please provide a description, explaining why this information is
    missing (e.g., because it was unavailable). This does not include
    intentionally removed information, but might include, e.g., redacted
    text.

    Some features (e.g., the country of origin in IPUMS Adult) contain
    missing values. We again refer to the respective documentation from
    the US Census Bureau for details.

-   **Are relationships between individual instances made explicit
    (e.g., users' movie ratings, social network links)?** If so, please
    describe how these relationships are made explicit.

    Our versions of the datasets contain no relationships between
    individuals. The original data sources from the US Census contain
    relationships between individuals and households.

-   **Are there recommended data splits (e.g., training,
    development/validation, testing)?** If so, please provide a
    description of these splits, explaining the rationale behind them.

    For IPUMS Adult, it is possible to follow the same train / test
    split as the original UCI Adult. In general, we recommend k-fold
    cross-validation for all of our datasets.

-   **Are there any errors, sources of noise, or redundancies in the
    dataset?** If so, please provide a description.

    Our IPUMS Adult reconstruction contains slightly more rows than the
    original UCI Adult, see Section 2 of the [associated
    paper](https://arxiv.org/abs/2108.04884).  Beyond IPUMS Adult, we refer to
    the documentation of CPS and ACS provided by the US Census Bureau.

-   **Is the dataset self-contained, or does it link to or otherwise
    rely on external resources (e.g., websites, tweets, other
    datasets)?** If it links to or relies on external resources, a) are
    there guarantees that they will exist, and remain constant, over
    time; b) are there official archival versions of the complete
    dataset (i.e., including the external resources as they existed at
    the time the dataset was created); c) are there any restrictions
    (e.g., licenses, fees) associated with any of the external resources
    that might apply to a future user? Please provide descriptions of
    all external resources and any restrictions associated with them, as
    well as links or other access points, as appropriate.

    Due to restrictions on the re-distribution of the original IPUMS and
    ACS data sources, we do not provide our datasets as standalone data
    files. Instead, we provide scripts to generate our datasets from the
    respective sources.

    Both the US Census Bureau and IPUMS aim to provide stable long-term
    access to their data. Hence we consider these data sources to be
    reliable. We refer to the IPUMS website and the website of the US
    Census Bureau for specific usage restrictions. Neither data source
    has fees associated with it.

-   **Does the dataset contain data that might be considered
    confidential (e.g., data that is protected by legal privilege or by
    doctor patient confidentiality, data that includes the content of
    individuals' non-public communications)?** If so, please provide a
    description.

    Our datasets are subsets of datasets released publicly by the US
    Census Bureau.

-   **Does the dataset contain data that, if viewed directly, might be
    offensive, insulting, threatening, or might otherwise cause
    anxiety?** If so, please describe why.

    No.

-   **Does the dataset relate to people?** If not, you may skip the
    remaining questions in this section.

    Yes, each instance in our datasets corresponds to a person.

-   **Does the dataset identify any subpopulations (e.g., by age,
    gender)?** If so, please describe how these subpopulations are
    identified and provide a description of their respective
    distributions within the dataset.

    Our datasets identify subpopulations since each individual has
    features such as age, gender, or race. Please see the main text of
    our paper for experiments exploring the respective distributions.

-   **Is it possible to identify individuals (i.e., one or more natural
    persons), either directly or indirectly (i.e., in combination with
    other data) from the dataset?** If so, please describe how.

    To the best of our knowledge, it is not possible to identify
    individuals *directly* from our datasets. However, the possibility
    of reconstruction attacks combining data from the US Cenus Bureau
    (such as CPS and ACS) and other data sources are a concern and
    actively investigated by the research community.

-   **Does the dataset contain data that might be considered sensitive
    in any way (e.g., data that reveals racial or ethnic origins, sexual
    orientations, religious beliefs, political opinions or union
    memberships, or locations; financial or health data; biometric or
    genetic data; forms of government identification, such as social
    security numbers; criminal history)?** If so, please provide a
    description.

    Our datasets contain features such as race, age, or gender that are
    often considered sensitive. This is by design since we assembled our
    datasets to test algorithmic fairness interventions.

-   **Any other comments?**

    No.

Collection process
------------------

-   **How was the data associated with each instance acquired?** Was the
    data directly observable (e.g., raw text, movie ratings), reported
    by subjects (e.g., survey responses), or indirectly inferred/derived
    from other data (e.g., part-of-speech tags, model-based guesses for
    age or language)? If data was reported by subjects or indirectly
    inferred/derived from other data, was the data validated/verified?
    If so, please describe how.

    The data was reported by subjects as part of the ACS and CPS
    surveys. The respective documentation provided by the US Census
    Bureau contains further information, see
    <https://www.census.gov/programs-surveys/acs/methodology/design-and-methodology.html>
    and
    <https://www.census.gov/programs-surveys/cps/technical-documentation/methodology.html>.

-   **What mechanisms or procedures were used to collect the data (e.g.,
    hardware apparatus or sensor, manual human curation, software
    program, software API)?** How were these mechanisms or procedures
    validated?

    The ACS relies on a combination of internet, mail, telephone, and
    in-person interviews. CPS uses in-person and telephone interviews.
    Please see the aforementioned documentation from the US Census
    Bureau for detailed information.

-   **If the dataset is a sample from a larger set, what was the
    sampling strategy (e.g., deterministic, probabilistic with specific
    sampling probabilities)?**

    For the ACS, the US Census Bureau sampled housing units uniformly
    for each county. See Chapter 4 in the ACS documentation
    (<https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/acs_design_methodology_report_2014.pdf>)
    for details.

    CPS is also sampled by housing unit from certain sampling areas, see
    Chapters 3 and 4 in
    <https://www.census.gov/prod/2006pubs/tp-66.pdf>.

-   **Who was involved in the data collection process (e.g., students,
    crowdworkers, contractors) and how were they compensated (e.g., how
    much were crowdworkers paid)?**

    The US Census Bureau employs interviewers for conducting surveys.
    According to online job information platforms such as
    [indeed.com](indeed.com), an interviewer earns about \$15 per hour.

-   **Over what timeframe was the data collected?** Does this timeframe
    match the creation timeframe of the data associated with the
    instances (e.g., recent crawl of old news articles)? If not, please
    describe the timeframe in which the data associated with the
    instances was created.

    Both CPS and ACS collect data annually. Our IPUMS Adult
    reconstruction contains data from the 1994 CPS ASEC. Our new tasks
    derived from ACS can be instantiated for various survey years.

-   **Were any ethical review processes conducted (e.g., by an
    institutional review board)?** If so, please provide a description
    of these review processes, including the outcomes, as well as a link
    or other access point to any supporting documentation.

    Both ACS and CPS are regularly reviewed by the US Census Bureau. As
    a government agency, the US Census Bureau is also subject to
    government oversight mechanisms.

-   **Does the dataset relate to people? If not, you may skip the
    remainder of the questions in this section.**

    Yes.

-   **Did you collect the data from the individuals in question
    directly, or obtain it via third parties or other sources (e.g.,
    websites)?**

    Data collection was performed by the US Census Bureau. We obtained
    the data from publicly available US Census repositories.

-   **Were the individuals in question notified about the data
    collection?** If so, please describe (or show with screenshots or
    other information) how notice was provided, and provide a link or
    other access point to, or otherwise reproduce, the exact language of
    the notification itself.

    Yes. A sample ACS form is available online:
    <https://www.census.gov/programs-surveys/acs/about/forms-and-instructions/2021-form.html>

    Information about the CPS collection methodology is available here:
    <https://www.census.gov/programs-surveys/cps/technical-documentation/methodology.html>

-   **Did the individuals in question consent to the collection and use
    of their data?** If so, please describe (or show with screenshots or
    other information) how consent was requested and provided, and
    provide a link or other access point to, or otherwise reproduce, the
    exact language to which the individuals consented.

    Participation in the US Census American Community Survey is
    mandatory. Participation in the US Corrent Population Survey is
    voluntary and consent is obtained at the beginning of the interview:
    <https://www2.census.gov/programs-surveys/cps/methodology/CPS-Tech-Paper-77.pdf>

-   **If consent was obtained, were the consenting individuals provided
    with a mechanism to revoke their consent in the future or for
    certain uses?** If so, please provide a description, as well as a
    link or other access point to the mechanism (if appropriate).

    We are not aware that the Census Bureau would provide such a
    mechanism.

-   **Has an analysis of the potential impact of the dataset and its use
    on data subjects (e.g., a data protection impact analysis) been
    conducted?** If so, please provide a description of this analysis,
    including the outcomes, as well as a link or other access point to
    any supporting documentation.

    The US Census Bureau assesses privacy risks and invests in
    statistical disclosure control. See
    <https://www.census.gov/topics/research/disclosure-avoidance.html>.
    Our derived prediction tasks do not increase privacy risks.

-   **Any other comments?**

    No.

Preprocessing / cleaning / labeling
-----------------------------------

-   **Was any preprocessing/cleaning/labeling of the data done (e.g.,
    discretization or bucketing, tokenization, part-of-speech tagging,
    SIFT feature extraction, removal of instances, processing of missing
    values)?** If so, please provide a description. If not, you may skip
    the remainder of the questions in this section.

    We used two US Census data products -- we reconstructed UCI Adult
    from the Annual Social and Economic Supplement (ASEC) of the Current
    Population Survey (CPS), and we constructed new prediction tasks
    from the American Community Survey (ACS) Public Use Microdata Sample
    (PUMS). Before releasing CPS data publicly, the Census Bureau
    top-codes certain variables and conducts imputation of certain
    missing values, as documented here:
    <https://www.census.gov/programs-surveys/cps/technical-documentation/methodology.html>.
    In our IPUMS Adult reconstruction, we include a subset of the
    variables available from the CPS data and do not alter their values.

    The ACS data release similarly top-codes certain variables and
    conducts imputation of certain missing values, as documented here:
    <https://www.census.gov/programs-surveys/acs/microdata/documentation.html>.
    For the new prediction tasks that we define, we further process the
    ACS data as documented at the folktables GitHub page,
    <https://github.com/zykls/folktables>. In most cases, this involves
    mapping missing values (NaNs) to -1. We release code so that new
    prediction tasks may be defined on the ACS data, with potentially
    different preprocessing. Each prediction task also defines a binary
    label by discretizing the target variable into two classes; this can
    be easily changed to define a new labeling in a new prediction task.

-   **Was the "raw" data saved in addition to the
    preprocessed/cleaned/labeled data (e.g., to support unanticipated
    future uses)?** If so, please provide a link or other access point
    to the "raw" data.

    Yes, our package provides access to the data as released by the U.S.
    Census Bureau. The "raw" survey answers collected by the Census
    Bureau are not available for public release due to privacy
    considerations.

-   **Is the software used to preprocess/clean/label the instances
    available?** If so, please provide a link or other access point.

    The software to is available at the folktables GitHub page,
    <https://github.com/zykls/folktables>.

-   **Any other comments?**

    No.

Uses
----

-   **Has the dataset been used for any tasks already?** If so, please
    provide a description.

    In this paper we create five new prediction tasks from the ACS PUMS
    data:

    1.  ACSIncome: Predict whether US working adults' yearly income is
        above \$50,000.

    2.  ACSPublicCoverage: Predict whether a low-income individual, not
        eligible for Medicare, has coverage from public health
        insurance.

    3.  ACSMobility: Predict whether a young adult moved addresses in
        the last year.

    4.  ACSEmployment: Predict whether a US adult is employed.

    5.  ACSTravelTime: Predict whether a working adult has a travel time
        to work of greater than 20 minutes.

    Further details about these tasks can be found at the folktables
    GitHub page, <https://github.com/zykls/folktables>, and in Appendix
    [\[appendix:new-tasks\]](#appendix:new-tasks){reference-type="ref"
    reference="appendix:new-tasks"}.

-   **Is there a repository that links to any or all papers or systems
    that use the dataset?** If so, please provide a link or other access
    point.

    At the folktables GitHub page,
    <https://github.com/zykls/folktables>, any public forks to the
    package are visible, and papers or systems that use the datasets
    should cite the paper linked at that Github page.

-   **What (other) tasks could the dataset be used for?**

    New prediction tasks may be defined on the ACS PUMS data that use
    different subsets of variables as features and/or different target
    variables. Different prediction tasks may have different properties
    such as Bayes error rate, or the base rate disparities between
    subgroups, that can help to benchmark machine learning models in
    diverse settings.

-   **Is there anything about the composition of the dataset or the way
    it was collected and preprocessed/cleaned/labeled that might impact
    future uses?** For example, is there anything that a future user
    might need to know to avoid uses that could result in unfair
    treatment of individuals or groups (e.g., stereotyping, quality of
    service issues) or other undesirable harms (e.g., financial harms,
    legal risks) If so, please provide a description. Is there anything
    a future user could do to mitigate these undesirable harms?

    Both the CPS and ACS are collected through surveys of a subset of
    the US population, and in their documentation, they acknowledge that
    statistical trends in individual states may be noisy compared to
    those found by analyzing US data as a whole, due to small sample
    sizes in certain states. In particular, there may be very few
    individuals with particular characteristics (e.g. ethnicity) in
    certain states, and generalizing conclusions from these few
    individuals may be highly inaccurate. Further, benchmarking fair
    machine learning algorithms on datasets with few representatives of
    certain subgroups may provide the illusion of "checking a box" for
    fairness, without substantive merit.

-   **Are there tasks for which the dataset should not be used?** If so,
    please provide a description.

    This dataset contains personal information, and users should not
    attempt to re-identify individuals in it. Further, these datasets
    are meant primarily to aid in benchmarking machine learning
    algorithms; Census data is often crucial for substantive,
    domain-specific work by social scientists, but our dataset
    contributions are not in this direction. Substantive investigations
    into inequality, demographic shifts, and other important questions
    should not be based purely on the datasets we provide.

-   **Any other comments?**

    No.

Distribution
------------

-   **Will the dataset be distributed to third parties outside of the
    entity (e.g., company, institution, organization) on behalf of which
    the dataset was created?** If so, please provide a description.

    The dataset will be available for public download on the folktables
    GitHub page, <https://github.com/zykls/folktables>.

-   **How will the dataset will be distributed (e.g., tarball on
    website, API, GitHub)?** Does the dataset have a digital object
    identifier (DOI)?

    The dataset will be be distributed via GitHub, see
    <https://github.com/zykls/folktables>. The dataset does not have a
    DOI.

-   **When will the dataset be distributed?**

    The dataset will be released on August 1, 2021 and available
    thereafter for download and public use.

-   **Will the dataset be distributed under a copyright or other
    intellectual property (IP) license, and/or under applicable terms of
    use (ToU)?** If so, please describe this license and/or ToU, and
    provide a link or other access point to, or otherwise reproduce, any
    relevant licensing terms or ToU, as well as any fees associated with
    these restrictions.

    The folktables package and data loading code will be available under
    the MIT license. The folktables data itself is based on data from
    the American Community Survey (ACS) Public Use Microdata Sample
    (PUMS) files managed by the US Census Bureau, and it is governed by
    the terms of use provided by the Census Bureau. For more
    information, see
    <https://www.census.gov/data/developers/about/terms-of-service.html>

    Similarly, the IPUMS adult reconstruction is governed by the IPUMS
    terms of use. For more information, see
    <https://ipums.org/about/terms>.

-   **Have any third parties imposed IP-based or other restrictions on
    the data associated with the instances?** If so, please describe
    these restrictions, and provide a link or other access point to, or
    otherwise reproduce, any relevant licensing terms, as well as any
    fees associated with these restrictions.

    The folktables data and the adult reconstruction data are governed
    by third-party terms of use provided by the US Census Bureau and
    IPUMS, respectively. See
    <https://www.census.gov/data/developers/about/terms-of-service.html>
    and <https://ipums.org/about/terms> for complete details. The IPUMS
    Adult Reconstruction is a subsample of the IPUMS CPS data available
    from [cps.ipums.org](cps.ipums.org) These data are intended for
    replication purposes only. Individuals analyzing the data for other
    purposes must submit a separate data extract request directly via
    IPUMS CPS. Individuals should contact
    [ipums\@umn.edu](ipums@umn.edu) for redistribution requests.

-   **Do any export controls or other regulatory restrictions apply to
    the dataset or to individual instances?** If so, please describe
    these restrictions, and provide a link or other access point to, or
    otherwise reproduce, any supporting documentation.

    To our knowledge, no export controls or regulatory restrictions
    apply to the dataset.

-   **Any other comments?**

    No.

Maintenance
-----------

-   **Who is supporting/hosting/maintaining the dataset?**

    The dataset will be hosted on GitHub, and supported and maintained
    by the folktables team. As of June 2021, this team consists of
    Frances Ding, Moritz Hardt, John Miller, and Ludwig Schmidt.

-   **How can the owner/curator/manager of the dataset be contacted
    (e.g., email address)?**

    Please send issues and requests to
    [folktables\@gmail.com](folktables@gmail.com).

-   **Is there an erratum?** If so, please provide a link or other
    access point.

    An erratum will be hosted on the dataset website,
    <https://github.com/zykls/folktables>.

-   **Will the dataset be updated (e.g., to correct labeling errors, add
    new instances, delete instances)?** If so, please describe how
    often, by whom, and how updates will be communicated to users (e.g.,
    mailing list, GitHub)?

    The dataset will be updated as required to address errors and refine
    the prediction problems based on feedback from the community. The
    package maintainers will update the dataset and communicate these
    updates on GitHub.

-   **If the dataset relates to people, are there applicable limits on
    the retention of the data associated with the instances (e.g., were
    individuals in question told that their data would be retained for a
    fixed period of time and then deleted)?** If so, please describe
    these limits and explain how they will be enforced.

    The data used in folktables is based on data from the American
    Community Survey (ACS) Public Use Microdata Sample (PUMS) files
    managed by the US Census Bureau. The data inherits and will respect
    the corresponding retention policies of the ACS. Please see
    <https://www.census.gov/programs-surveys/acs/about.html> for more
    details. For the Adult reconstruction dataset, the data is based on
    Current Population Survey (CPS) released by IPUMS and thus inherits
    and will respect the corresponding retention policies for the CPS.
    Please see <https://cps.ipums.org/cps/> for more details.

-   **Will older versions of the dataset continue to be
    supported/hosted/maintained?** If so, please describe how. If not,
    please describe how its obsolescence will be communicated to users.

    Older versions of the datasets in folktables will be clearly
    indicated, supported, and maintained on the GitHub website. Each new
    version of the dataset will be tagged with version metadata and an
    associated GitHub release.

-   **If others want to extend/augment/build on/contribute to the
    dataset, is there a mechanism for them to do so?** If so, please
    provide a description. Will these contributions be
    validated/verified? If so, please describe how. If not, why not? Is
    there a process for communicating/distributing these contributions
    to other users? If so, please provide a description.

    Users wishing to contribute to folktables datasets are encouraged to
    do so by submitting a pull request on the website
    <https://github.com/zykls/folktables/pulls>. The contributions will
    be reviewed by the maintainers. These contributions will be
    reflected in new version of the dataset and broadcasted as part of
    each Github release.

-   **Any other comments?**

    No.
