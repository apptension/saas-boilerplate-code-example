import { Story } from '@storybook/react';
import { createMockEnvironment } from 'relay-test-utils';

import { ProvidersWrapper } from '../../utils/testUtils';
import { currentUserFactory } from '../../../mocks/factories';
import { CurrentUserType } from '../../services/graphqlApi/__generated/types';
import { fillCommonQueryWithUser } from '../../utils/commonQuery';
import { Avatar, AvatarProps } from './avatar.component';

type StoryArgsType = AvatarProps & { profile: CurrentUserType };

const Template: Story<StoryArgsType> = ({ profile, ...args }: StoryArgsType) => {
  const relayEnvironment = createMockEnvironment();
  fillCommonQueryWithUser(relayEnvironment, profile);
  return (
    <ProvidersWrapper
      context={{
        relayEnvironment,
      }}
    >
      <Avatar {...args} />
    </ProvidersWrapper>
  );
};

export default {
  title: 'Shared/Avatar',
  component: Avatar,
};

export const Default = Template.bind({});

export const NoAvatarUser = Template.bind({});
NoAvatarUser.args = { profile: currentUserFactory({ avatar: null }) };

export const NoNameUser = Template.bind({});
NoNameUser.args = { profile: currentUserFactory({ firstName: '', lastName: '', avatar: null }) };

export const CustomSize = Template.bind({});
CustomSize.args = { size: 100 };
