@Library("github.com/RedHatInsights/insights-pipeline-lib") _

node {
    cancelPriorBuilds()

    podParameters = [
        slaveConnectTimeout: 120,
        instanceCap: 10,
        cloud: pipelineVars.defaultUICloud,
        namespace: pipelineVars.defaultUINameSpace,
        annotations: [
           podAnnotation(key: "job-name", value: "${env.JOB_NAME}"),
           podAnnotation(key: "run-display-url", value: "${env.RUN_DISPLAY_URL}"),
        ],
    ]


    // def browsers = ["chrome", "firefox"] // labels for Jenkins node types we will build on
    // def builders = [:]
    // for (x in browsers) {
    //     def browser = x // Need to bind the label variable before the closure - can't do 'for (label in labels)'
    //     def label = "test-${UUID.randomUUID().toString()}"

    //     // Create a map to pass in to the 'parallel' step so we can fire all the builds at once
    //     builders[browser] = {
    //         podParameters["annotations"].add(podAnnotation(key: "browser", value: browser))
    //         podParameters["label"] = label
    //         podParameters["containers"] = [
    //             containerTemplate(
    //                 name: "jnlp",
    //                 image: "docker-registry.engineering.redhat.com/centralci/jnlp-slave-base:1.5",
    //                 args: '${computer.jnlpmac} ${computer.name}',
    //                 resourceRequestCpu: "250m",
    //                 resourceLimitCpu: "500m",
    //                 resourceRequestMemory: "512Mi",
    //                 resourceLimitMemory: "1Gi",
    //             ),
    //             containerTemplate(
    //                 name: "python",
    //                 ttyEnabled: true,
    //                 command: "cat",
    //                 image: "docker-registry.upshift.redhat.com/insights-qe/python-slim:latest",
    //                 resourceRequestCpu: "250m",
    //                 resourceLimitCpu: "500m",
    //                 resourceRequestMemory: "512Mi",
    //                 resourceLimitMemory: "1Gi",
    //             ),
    //             containerTemplate(
    //                 name: "selenium",
    //                 image: pipelineVars.seleniumImage,
    //                 resourceRequestCpu: "750m",
    //                 resourceLimitCpu: "1",
    //                 resourceRequestMemory: "2Gi",
    //                 resourceLimitMemory: "4Gi",
    //             ),
    //         ]
    //         podTemplate(podParameters) {
    //             node(label) {
    //                 container("python") {
    //                     checkout scm

    //                     stageWithContext("install") {
    //                         sh "python setup.py install"
    //                     }

    //                     stageWithContext("linting") {
    //                         sh "flake8 src testing --max-line-length=100"
    //                     }

    //                     stageWithContext("test") {
    //                         withEnv(["BROWSER=remote_${browser}"]) {
    //                             sh "pytest -v --no-cov-on-fail --cov=widgetastic_patternfly4 --junitxml=junit.xml"
    //                         }
    //                     }
    //                     withCredentials([string(credentialsId: "wt.pf4_codecov_token", variable: "CODECOV_TOKEN")]) {
    //                         sh "codecov"
    //                     }
    //                     junit "junit.xml"
    //                 }
    //             }
    //         }
    //     }
    // }
    // parallel builders
    checkout scm
    def tag = sh(returnStdout: true, script: "git tag --contains | head -1").trim()
    if (tag) {
        def label = "test-${UUID.randomUUID().toString()}"
        podParameters["label"] = label
        podParameters["containers"] = [
            containerTemplate(
                name: "jnlp",
                image: "docker-registry.engineering.redhat.com/centralci/jnlp-slave-base:1.5",
                args: '${computer.jnlpmac} ${computer.name}',
                resourceRequestCpu: "250m",
                resourceLimitCpu: "500m",
                resourceRequestMemory: "512Mi",
                resourceLimitMemory: "1Gi",
            ),
            containerTemplate(
                name: "python",
                ttyEnabled: true,
                command: "cat",
                image: "docker-registry.upshift.redhat.com/insights-qe/python-slim:latest",
                resourceRequestCpu: "100m",
                resourceLimitCpu: "200m",
                resourceRequestMemory: "256Mi",
                resourceLimitMemory: "512Mi",
            ),
        ]
        podTemplate(podParameters) {
            node(label) {
                container("python") {
                    checkout scm

                    stage("upload-to-pypi") {
                        withCredentials([usernamePassword(
                            credentialsId: "pypi",
                            usernameVariable: "TWINE_USERNAME",
                            passwordVariable: "TWINE_PASSWORD"
                        )]){
                            sh "python setup.py sdist bdist_wheel"
                            sh "twine upload dist/*"
                        }
                    }
                }
            }
        }
    }
}
