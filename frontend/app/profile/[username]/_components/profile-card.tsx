import { Card, CardContent, CardHeader } from '@/common/components/ui/card'
import { UserProfileDTO } from '@/data-access/dto/user.dto'
import React from 'react'

const ProfileCard = ({ user}: { user: UserProfileDTO }) => {
  return (
    <Card className='mb-12'>
      <CardHeader>
        <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-6">
          <div className="space-y-4 flex-1">
            <div>
              <h1 className="text-3xl sm:text-4xl font-bold">
                {user.first_name} {user.last_name}
              </h1>
              <p className="text-muted-foreground mt-1">
                @{user.username}
              </p>
            </div>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-3 gap-4">
          <div className="space-y-1 text-center">
            <p className="text-2xl sm:text-3xl font-bold">
              {user.blog_count.total_blogs}
            </p>
            <p className="text-xs sm:text-sm text-muted-foreground">
              Total Blogs
            </p>
          </div>


          <div className="space-y-1 text-center">
            <p className="text-2xl sm:text-3xl font-bold">
              {user.blog_count.published_blogs} 
            </p>
            <p className="text-xs sm:text-sm text-muted-foreground">
              Published 
            </p>
          </div>


          <div className="space-y-1 text-center">
            <p className="text-2xl sm:text-3xl font-bold">
              {user.blog_count.draft_blogs}
            </p>
            <p className="text-xs sm:text-sm text-muted-foreground">
              Drafts 
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

export default ProfileCard 