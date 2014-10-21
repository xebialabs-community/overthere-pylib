/**
 * THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
 * FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
 */

package com.xebialabs.deployit.plugin.otpylib;

import java.net.URISyntaxException;
import java.net.URL;
import org.junit.Test;

import com.xebialabs.overthere.OverthereFile;
import com.xebialabs.overthere.local.LocalConnection;

import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.CoreMatchers.notNullValue;
import static org.hamcrest.MatcherAssert.assertThat;

public class DirectoryDiffTest {

    private OverthereFile file(String name) throws URISyntaxException {
        URL resource = Thread.currentThread().getContextClassLoader().getResource(name);
        assertThat("File " + name + "not found", resource, notNullValue());
        return LocalConnection.getLocalConnection().getFile(resource.getPath());
    }

    @Test
    public void shouldDiffDirectories() throws Exception{

        OverthereFile leftDir = file("directorycompare/old");
        OverthereFile rightDir = file("directorycompare/new");

        DirectoryDiff diff = new DirectoryDiff(leftDir,rightDir);
        DirectoryDiff.DirectoryChangeSet changeSet = diff.diff();

        System.out.println("Changed files : " + changeSet.getChanged());
        assertThat(changeSet.getChanged().size(), equalTo(2));
        System.out.println("Removed files : " + changeSet.getRemoved());
        assertThat(changeSet.getRemoved().size(), equalTo(3));
        System.out.println("Added files : " + changeSet.getAdded());
        assertThat(changeSet.getAdded().size(), equalTo(3));




    }
}
