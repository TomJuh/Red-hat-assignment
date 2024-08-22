XML_VALID= '''<testsuites name="Test run" tests="8" failures="1" errors="1" skipped="1" 
    assertions="20" time="16.082687" timestamp="2021-04-02T15:48:23">
    <testsuite name="Tests.Registration" tests="8" failures="1" errors="1" skipped="1" 
        assertions="20" time="16.082687" timestamp="2021-04-02T15:48:23" 
        file="tests/registration.code">

        <!-- <properties> Test suites (and test cases, see below) can have additional 
        properties such as environment variables or version numbers. -->
        <properties>
            <!-- <property> Each property has a name and value. Some tools also support
            properties with text values instead of value attributes. -->
            <property name="version" value="1.774" />
            <property name="commit" value="ef7bebf" />
            <property name="browser" value="Google Chrome" />
            <property name="ci" value="https://github.com/actions/runs/1234" />
            <property name="config">
                Config line #1
                Config line #2
                Config line #3
            </property>
        </properties>

        <testcase name="testCase1" classname="Tests.Registration" assertions="2"
            time="2.436" file="tests/registration.code" line="24" />
        <testcase name="testCase2" classname="Tests.Registration" assertions="6"
            time="1.534" file="tests/registration.code" line="62" />
        <testcase name="testCase3" classname="Tests.Registration" assertions="3"
            time="0.822" file="tests/registration.code" line="102" />
        
        <testcase name="testCase4" classname="Tests.Registration" assertions="0"
            time="0" file="tests/registration.code" line="164">
            <!-- <skipped> Indicates that the test was not executed. Can have an optional
            message describing why the test was skipped. -->
            <skipped message="Test was skipped." />
        </testcase>

        <!-- Example of a test case that failed. -->
        <testcase name="testCase5" classname="Tests.Registration" assertions="2"
            time="2.902412" file="tests/registration.code" line="202">
            <!-- <failure> The test failed because one of the assertions/checks failed.
            Can have a message and failure type, often the assertion type or class. The text
            content of the element often includes the failure description or stack trace. -->
            <failure message="Expected value did not match." type="AssertionError">
                <!-- Failure description or stack trace -->
            </failure>
        </testcase>

        <!-- Example of a test case that had errors. -->
        <testcase name="testCase6" classname="Tests.Registration" assertions="0"
            time="3.819" file="tests/registration.code" line="235">
            <!-- <error> The test had an unexpected error during execution. Can have a 
            message and error type, often the exception type or class. The text
            content of the element often includes the error description or stack trace. -->
            <error message="Division by zero." type="ArithmeticError">
                <!-- Error description or stack trace -->
            </error>
        </testcase>

        <!-- Example of a test case with outputs. -->
        <testcase name="testCase7" classname="Tests.Registration" assertions="3"
            time="2.944" file="tests/registration.code" line="287">
            <!-- <system-out> Optional data written to standard out for the test case. -->
            <system-out>Data written to standard out.</system-out>

            <!-- <system-err> Optional data written to standard error for the test case. -->
            <system-err>Data written to standard error.</system-err>
        </testcase>

            <!-- Example of a test case with properties -->
            <testcase name="testCase8" classname="Tests.Registration" assertions="4"
                time="1.625275" file="tests/registration.code" line="302">
                <!-- <properties> Some tools also support properties for test cases. -->
                <properties>
                    <property name="priority" value="high" />
                    <property name="language" value="english" />
                    <property name="author" value="Adrian" />
                    <property name="attachment" value="screenshots/dashboard.png" />
                    <property name="attachment" value="screenshots/users.png" />
                    <property name="description">
                        This text describes the purpose of this test case and provides
                        an overview of what the test does and how it works.
                    </property>
                </properties>
            </testcase>
        </testsuite>
    </testsuites>
'''
XML_ERORS='''
<testsuites time="15.682687">
    <testsuite name="Tests.Registration" time="6.605871">
        <testcase name="testCase1" classname="Tests.Registration" time="2.113871" />
        <testcase name="testCase2" classname="Tests.Registration" time="1.051" />
        <testcaser name="testCase3" classname="Tests.Registration" time="3.441" />
    </testsuite>
    <testsuite name="Tests.Authentication" time="9.076816">
        <testsuite name="Tests.Authentication.Login" time="4.356">
            <testcase name="testCase4" classname="Tests.Authentication.Login" time="2.244" />
            <testcase name="testCase5" classname="Tests.Authentication.Login" time="0.781" />
            <testcase name="testCase6" classname="Tests.Authentication.Login" time="1.331" />
        </testsuite>
        <testcase name="testCase7" classname="Tests.Authentication" time="2.508" />
        <testcase name="testCase8" classname="Tests.Authentication" time="1.230816" />
        <testcase name="testCase9" classname="Tests.Authentication" time="0.982">
            <failurer message="Assertion error message" type="AssertionError">
            </failurer>            
        </testcase>
    </testsuite>
</testsuites>
'''